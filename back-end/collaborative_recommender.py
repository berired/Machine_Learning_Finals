import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.decomposition import NMF
from scipy.sparse import csr_matrix
import joblib

class CollaborativeFilteringRecommender:
    """
    Implements collaborative filtering for financial recommendations.
    Uses user-item interaction data to recommend products based on similar users' preferences.
    """
    
    def __init__(self, n_components=10):
        self.n_components = n_components
        self.nmf_model = NMF(n_components=n_components, random_state=42)
        self.user_product_matrix = None
        self.user_features = None
        self.product_features = None
        self.user_similarity_matrix = None
        self.product_ids = None
        self.user_ids = None
        
    def create_user_product_interactions(self, user_data, product_recommendations):
        """
        Create user-product interaction matrix from historical data and recommendations.
        Since we don't have explicit ratings, we'll use implicit feedback.
        """
        interactions = []
        
        # Generate synthetic interaction data based on user profiles and recommendations
        for user_id, user_profile in enumerate(user_data):
            for product_rec in product_recommendations[user_id] if user_id < len(product_recommendations) else []:
                # Create implicit rating based on suitability score
                rating = min(5.0, max(1.0, product_rec['suitability_score'] * 5))
                
                interactions.append({
                    'user_id': user_id,
                    'product_id': product_rec['product_id'],
                    'rating': rating,
                    'category': product_rec['category']
                })
        
        return pd.DataFrame(interactions)
    
    def build_interaction_matrix(self, interactions_df):
        """Build user-product interaction matrix"""
        if interactions_df.empty:
            print("No interaction data available")
            return None
            
        # Create pivot table
        self.user_product_matrix = interactions_df.pivot_table(
            index='user_id', 
            columns='product_id', 
            values='rating', 
            fill_value=0
        )
        
        self.user_ids = self.user_product_matrix.index.tolist()
        self.product_ids = self.user_product_matrix.columns.tolist()
        
        print(f"Created interaction matrix: {self.user_product_matrix.shape}")
        return self.user_product_matrix
    
    def train_collaborative_model(self, interactions_df):
        """Train the collaborative filtering model using NMF"""
        if interactions_df.empty:
            print("No interaction data for training")
            return False
            
        # Build interaction matrix
        interaction_matrix = self.build_interaction_matrix(interactions_df)
        
        if interaction_matrix is None or interaction_matrix.empty:
            return False
        
        # Train NMF model
        try:
            self.user_features = self.nmf_model.fit_transform(interaction_matrix)
            self.product_features = self.nmf_model.components_
            
            # Calculate user similarity matrix
            self.user_similarity_matrix = cosine_similarity(self.user_features)
            
            print("Collaborative filtering model trained successfully")
            return True
            
        except Exception as e:
            print(f"Error training collaborative model: {e}")
            return False
    
    def find_similar_users(self, user_id, n_similar=5):
        """Find users similar to the given user"""
        if self.user_similarity_matrix is None or self.user_ids is None:
            return []
        
        if user_id not in self.user_ids:
            return []
        
        user_index = self.user_ids.index(user_id)
        similarities = self.user_similarity_matrix[user_index]
        
        # Get indices of most similar users (excluding self)
        similar_indices = np.argsort(similarities)[::-1][1:n_similar+1]
        
        similar_users = []
        for idx in similar_indices:
            if idx < len(self.user_ids):
                similar_users.append({
                    'user_id': self.user_ids[idx],
                    'similarity_score': similarities[idx]
                })
        
        return similar_users
    
    def recommend_products_collaborative(self, user_id, n_recommendations=5):
        """Generate product recommendations using collaborative filtering"""
        if (self.user_product_matrix is None or self.user_ids is None or 
            self.product_ids is None or user_id not in self.user_ids):
            return []
        
        user_index = self.user_ids.index(user_id)
        
        # Get user's current ratings
        user_ratings = self.user_product_matrix.iloc[user_index]
        
        # Find similar users
        similar_users = self.find_similar_users(user_id)
        
        if not similar_users:
            return []
        
        # Calculate weighted average ratings from similar users
        recommendations = {}
        
        for product_id in self.product_ids:
            if user_ratings[product_id] == 0:  # User hasn't interacted with this product
                weighted_sum = 0
                similarity_sum = 0
                
                for similar_user in similar_users:
                    similar_user_id = similar_user['user_id']
                    similarity_score = similar_user['similarity_score']
                    
                    if similar_user_id in self.user_ids:
                        similar_user_index = self.user_ids.index(similar_user_id)
                        similar_user_rating = self.user_product_matrix.iloc[similar_user_index][product_id]
                        
                        if similar_user_rating > 0:
                            weighted_sum += similarity_score * similar_user_rating
                            similarity_sum += similarity_score
                
                if similarity_sum > 0:
                    predicted_rating = weighted_sum / similarity_sum
                    recommendations[product_id] = predicted_rating
        
        # Sort recommendations by predicted rating
        sorted_recommendations = sorted(recommendations.items(), 
                                      key=lambda x: x[1], reverse=True)
        
        return sorted_recommendations[:n_recommendations]
    
    def hybrid_recommendation(self, user_id, content_recommendations, n_recommendations=5, 
                            content_weight=0.7, collaborative_weight=0.3):
        """
        Combine content-based and collaborative filtering recommendations
        """
        # Get collaborative recommendations
        collaborative_recs = self.recommend_products_collaborative(user_id, n_recommendations * 2)
        
        # Create combined score
        hybrid_recommendations = []
        
        # Start with content-based recommendations
        for content_rec in content_recommendations[:n_recommendations * 2]:
            product_id = content_rec['product_id']
            content_score = content_rec['suitability_score']
            
            # Find collaborative score for this product
            collaborative_score = 0
            for collab_rec in collaborative_recs:
                if collab_rec[0] == product_id:
                    collaborative_score = collab_rec[1] / 5.0  # Normalize to 0-1
                    break
            
            # Calculate hybrid score
            hybrid_score = (content_weight * content_score + 
                          collaborative_weight * collaborative_score)
            
            hybrid_rec = content_rec.copy()
            hybrid_rec['hybrid_score'] = hybrid_score
            hybrid_rec['collaborative_score'] = collaborative_score
            hybrid_recommendations.append(hybrid_rec)
        
        # Add purely collaborative recommendations that weren't in content-based
        content_product_ids = {rec['product_id'] for rec in content_recommendations}
        for collab_rec in collaborative_recs:
            product_id = collab_rec[0]
            if product_id not in content_product_ids:
                hybrid_recommendations.append({
                    'product_id': product_id,
                    'product_name': f'Product {product_id}',
                    'category': 'unknown',
                    'suitability_score': 0,
                    'collaborative_score': collab_rec[1] / 5.0,
                    'hybrid_score': collaborative_weight * (collab_rec[1] / 5.0),
                    'expected_return': 0,
                    'risk_level': 'unknown',
                    'description': 'Recommended by similar users'
                })
        
        # Sort by hybrid score
        hybrid_recommendations.sort(key=lambda x: x['hybrid_score'], reverse=True)
        
        return hybrid_recommendations[:n_recommendations]
    
    def get_user_preferences_insights(self, user_id):
        """Get insights about user preferences based on collaborative data"""
        if (self.user_product_matrix is None or self.user_ids is None or 
            user_id not in self.user_ids):
            return {}
        
        user_index = self.user_ids.index(user_id)
        user_ratings = self.user_product_matrix.iloc[user_index]
        
        # Find user's preferred categories and products
        preferred_products = user_ratings[user_ratings > 3].index.tolist()
        
        # Find similar users
        similar_users = self.find_similar_users(user_id)
        
        insights = {
            'preferred_products': preferred_products,
            'similar_users': similar_users,
            'total_interactions': (user_ratings > 0).sum(),
            'average_rating': user_ratings[user_ratings > 0].mean() if (user_ratings > 0).sum() > 0 else 0
        }
        
        return insights
    
    def analyze_product_popularity(self):
        """Analyze product popularity across all users"""
        if self.user_product_matrix is None or self.product_ids is None or self.user_ids is None:
            return {}
        
        # Calculate product statistics
        product_stats = {}
        
        for product_id in self.product_ids:
            product_ratings = self.user_product_matrix[product_id]
            non_zero_ratings = product_ratings[product_ratings > 0]
            
            product_stats[product_id] = {
                'total_interactions': len(non_zero_ratings),
                'average_rating': non_zero_ratings.mean() if len(non_zero_ratings) > 0 else 0,
                'popularity_score': len(non_zero_ratings) / len(self.user_ids)
            }
        
        return product_stats
    
    def cold_start_recommendation(self, new_user_profile, all_user_profiles, 
                                content_recommender, n_recommendations=5):
        """
        Handle cold start problem for new users without interaction history
        """
        # Find similar users based on profile features
        similar_users = self.find_similar_users_by_profile(new_user_profile, all_user_profiles)
        
        if not similar_users:
            # Fall back to content-based recommendations
            return content_recommender.recommend_products(new_user_profile, n_recommendations)
        
        # Get recommendations from similar users
        recommendations = {}
        
        for similar_user in similar_users[:3]:  # Top 3 similar users
            user_id = similar_user['user_id']
            similarity_score = similar_user['similarity_score']
            
            if (self.user_ids is not None and self.product_ids is not None and 
                user_id in self.user_ids and self.user_product_matrix is not None):
                user_index = self.user_ids.index(user_id)
                user_ratings = self.user_product_matrix.iloc[user_index]
                
                for product_id in self.product_ids:
                    rating = user_ratings[product_id]
                    if rating > 0:
                        if product_id not in recommendations:
                            recommendations[product_id] = 0
                        recommendations[product_id] += similarity_score * rating
        
        # Sort and return top recommendations
        sorted_recs = sorted(recommendations.items(), key=lambda x: x[1], reverse=True)
        
        return [{
            'product_id': product_id,
            'predicted_rating': score,
            'recommendation_type': 'cold_start_collaborative'
        } for product_id, score in sorted_recs[:n_recommendations]]
    
    def find_similar_users_by_profile(self, target_profile, all_user_profiles):
        """Find users with similar profiles for cold start scenarios"""
        similarities = []
        
        target_features = [
            target_profile.get('age', 30),
            target_profile.get('income', 50000),
            target_profile.get('dependents', 0),
            target_profile.get('savings_rate', 0.1),
            target_profile.get('debt_to_income', 0.3)
        ]
        
        for user_id, profile in enumerate(all_user_profiles):
            user_features = [
                profile.get('age', 30),
                profile.get('income', 50000),
                profile.get('dependents', 0),
                profile.get('savings_rate', 0.1),
                profile.get('debt_to_income', 0.3)
            ]
            
            # Calculate cosine similarity
            similarity = cosine_similarity(np.array([target_features]), np.array([user_features]))[0][0]
            similarities.append({
                'user_id': user_id,
                'similarity_score': similarity
            })
        
        # Sort by similarity
        similarities.sort(key=lambda x: x['similarity_score'], reverse=True)
        
        return similarities
    
    def save_model(self, filepath):
        """Save the collaborative filtering model"""
        model_data = {
            'nmf_model': self.nmf_model,
            'user_product_matrix': self.user_product_matrix,
            'user_features': self.user_features,
            'product_features': self.product_features,
            'user_similarity_matrix': self.user_similarity_matrix,
            'product_ids': self.product_ids,
            'user_ids': self.user_ids,
            'n_components': self.n_components
        }
        joblib.dump(model_data, filepath)
        print(f"Collaborative filtering model saved to {filepath}")
    
    def load_model(self, filepath):
        """Load a saved collaborative filtering model"""
        model_data = joblib.load(filepath)
        self.nmf_model = model_data['nmf_model']
        self.user_product_matrix = model_data['user_product_matrix']
        self.user_features = model_data['user_features']
        self.product_features = model_data['product_features']
        self.user_similarity_matrix = model_data['user_similarity_matrix']
        self.product_ids = model_data['product_ids']
        self.user_ids = model_data['user_ids']
        self.n_components = model_data['n_components']
        print(f"Collaborative filtering model loaded from {filepath}")
