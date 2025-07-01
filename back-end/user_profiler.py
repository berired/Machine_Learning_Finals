import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.metrics import silhouette_score
import matplotlib.pyplot as plt
import seaborn as sns
import joblib

class UserProfiler:
    """
    Creates user profiles using clustering techniques to group similar financial behaviors.
    """
    
    def __init__(self, n_clusters=5):
        self.n_clusters = n_clusters
        self.kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
        self.pca = PCA(n_components=2)
        self.cluster_labels = None
        self.cluster_centers = None
        self.feature_names = None
        
    def find_optimal_clusters(self, data, max_clusters=10):
        """Find optimal number of clusters using elbow method and silhouette analysis"""
        if data.empty or len(data) < 4:
            print("Insufficient data for clustering")
            return 3
            
        inertias = []
        silhouette_scores = []
        k_range = range(2, min(max_clusters + 1, len(data)))
        
        for k in k_range:
            if k >= len(data):
                continue
                
            kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
            cluster_labels = kmeans.fit_predict(data)
            
            inertias.append(kmeans.inertia_)
            
            # Calculate silhouette score
            if len(np.unique(cluster_labels)) > 1:
                sil_score = silhouette_score(data, cluster_labels)
                silhouette_scores.append(sil_score)
            else:
                silhouette_scores.append(0)
        
        # Find elbow point (simplified)
        if len(silhouette_scores) > 0:
            optimal_k = k_range[np.argmax(silhouette_scores)]
        else:
            optimal_k = 3
            
        print(f"Optimal number of clusters: {optimal_k}")
        return optimal_k
    
    def create_user_clusters(self, data):
        """Create user clusters based on financial behavior"""
        if data.empty:
            print("No data available for clustering")
            return None
            
        # Remove non-numeric columns for clustering
        numeric_data = data.select_dtypes(include=[np.number])
        
        if numeric_data.empty:
            print("No numeric data available for clustering")
            return None
        
        self.feature_names = numeric_data.columns.tolist()
        
        # Find optimal number of clusters
        optimal_k = self.find_optimal_clusters(numeric_data)
        self.n_clusters = optimal_k
        self.kmeans = KMeans(n_clusters=optimal_k, random_state=42, n_init=10)
        
        # Fit clustering model
        self.cluster_labels = self.kmeans.fit_predict(numeric_data)
        self.cluster_centers = self.kmeans.cluster_centers_
        
        # Add cluster labels to original data
        data_with_clusters = data.copy()
        data_with_clusters['user_cluster'] = self.cluster_labels
        
        return data_with_clusters
    
    def analyze_clusters(self, data_with_clusters):
        """Analyze and interpret cluster characteristics"""
        if data_with_clusters is None or data_with_clusters.empty:
            return {}
            
        cluster_analysis = {}
        numeric_cols = data_with_clusters.select_dtypes(include=[np.number]).columns
        numeric_cols = [col for col in numeric_cols if col != 'user_cluster']
        
        for cluster_id in range(self.n_clusters):
            cluster_data = data_with_clusters[data_with_clusters['user_cluster'] == cluster_id]
            
            if cluster_data.empty:
                continue
                
            cluster_stats = {}
            
            # Calculate mean values for each feature
            for col in numeric_cols:
                if col in cluster_data.columns:
                    cluster_stats[col] = {
                        'mean': cluster_data[col].mean(),
                        'std': cluster_data[col].std(),
                        'median': cluster_data[col].median()
                    }
            
            cluster_stats['size'] = len(cluster_data)
            cluster_stats['percentage'] = len(cluster_data) / len(data_with_clusters) * 100
            
            cluster_analysis[f'cluster_{cluster_id}'] = cluster_stats
        
        return cluster_analysis
    
    def interpret_clusters(self, cluster_analysis):
        """Provide human-readable interpretations of clusters"""
        interpretations = {}
        
        for cluster_name, stats in cluster_analysis.items():
            cluster_id = cluster_name.split('_')[1]
            interpretation = {
                'profile_type': self._determine_profile_type(stats),
                'characteristics': self._extract_key_characteristics(stats),
                'size': stats.get('size', 0),
                'percentage': stats.get('percentage', 0)
            }
            interpretations[cluster_name] = interpretation
        
        return interpretations
    
    def _determine_profile_type(self, stats):
        """Determine user profile type based on cluster statistics"""
        # Simple rule-based classification (can be enhanced)
        income_indicators = ['Income', 'total_income', 'Credit_Limit']
        spending_indicators = ['total_expense', 'Total_Trans_Amt', 'Groceries', 'Transport']
        savings_indicators = ['savings_rate', 'Desired_Savings_Percentage', 'Disposable_Income']
        
        high_income = any(stats.get(ind, {}).get('mean', 0) > 0.5 for ind in income_indicators if ind in stats)
        high_spending = any(stats.get(ind, {}).get('mean', 0) > 0.5 for ind in spending_indicators if ind in stats)
        high_savings = any(stats.get(ind, {}).get('mean', 0) > 0.3 for ind in savings_indicators if ind in stats)
        
        if high_income and high_savings:
            return "Conservative High Earner"
        elif high_income and high_spending:
            return "Affluent Spender"
        elif high_savings:
            return "Prudent Saver"
        elif high_spending:
            return "Active Consumer"
        else:
            return "Budget Conscious"
    
    def _extract_key_characteristics(self, stats):
        """Extract key characteristics from cluster statistics"""
        characteristics = []
        
        # Analyze spending patterns
        spending_categories = ['Groceries', 'Transport', 'Entertainment', 'food_spending']
        for category in spending_categories:
            if category in stats and stats[category].get('mean', 0) > 0.3:
                characteristics.append(f"High {category.lower()} spending")
        
        # Analyze financial behavior
        if 'savings_rate' in stats and stats['savings_rate'].get('mean', 0) > 0.2:
            characteristics.append("Good savings rate")
        
        if 'Avg_Utilization_Ratio' in stats and stats['Avg_Utilization_Ratio'].get('mean', 0) > 0.5:
            characteristics.append("High credit utilization")
        
        return characteristics if characteristics else ["Balanced financial behavior"]
    
    def visualize_clusters(self, data_with_clusters, save_path=None):
        """Create visualizations for cluster analysis"""
        if data_with_clusters is None or data_with_clusters.empty:
            print("No data available for visualization")
            return
            
        numeric_data = data_with_clusters.select_dtypes(include=[np.number])
        numeric_data = numeric_data.drop('user_cluster', axis=1, errors='ignore')
        
        if numeric_data.empty or len(numeric_data.columns) < 2:
            print("Insufficient numeric data for visualization")
            return
        
        # Create PCA visualization
        try:
            pca_data = self.pca.fit_transform(numeric_data)
            
            plt.figure(figsize=(12, 8))
            
            # PCA scatter plot
            plt.subplot(2, 2, 1)
            scatter = plt.scatter(pca_data[:, 0], pca_data[:, 1], 
                                c=data_with_clusters['user_cluster'], 
                                cmap='viridis', alpha=0.6)
            plt.xlabel('First Principal Component')
            plt.ylabel('Second Principal Component')
            plt.title('User Clusters in PCA Space')
            plt.colorbar(scatter)
            
            # Cluster size distribution
            plt.subplot(2, 2, 2)
            cluster_sizes = data_with_clusters['user_cluster'].value_counts().sort_index()
            plt.bar(cluster_sizes.index, cluster_sizes.values)
            plt.xlabel('Cluster ID')
            plt.ylabel('Number of Users')
            plt.title('Cluster Size Distribution')
            
            # Feature importance heatmap (cluster centers)
            plt.subplot(2, 1, 2)
            if hasattr(self, 'cluster_centers') and self.cluster_centers is not None:
                # Take top features for better visualization
                if self.feature_names is not None:
                    n_features = min(10, len(self.feature_names))
                    top_features = self.feature_names[:n_features]
                    centers_subset = self.cluster_centers[:, :n_features]
                else:
                    n_features = 0
                    top_features = []
                    centers_subset = np.array([])
                
                sns.heatmap(centers_subset, 
                           xticklabels=top_features,
                           yticklabels=[f'Cluster {i}' for i in range(self.n_clusters)],
                           annot=True, cmap='coolwarm', center=0)
                plt.title('Cluster Centers (Standardized Values)')
            
            plt.tight_layout()
            
            if save_path:
                plt.savefig(save_path, dpi=300, bbox_inches='tight')
            else:
                plt.savefig('cluster_analysis.png', dpi=300, bbox_inches='tight')
            
            plt.show()
            
        except Exception as e:
            print(f"Error creating visualizations: {e}")
    
    def predict_user_cluster(self, user_data):
        """Predict cluster for a new user"""
        if self.kmeans is None:
            raise ValueError("Model not trained. Please run create_user_clusters first.")
        
        # Ensure user_data has the same features as training data
        if isinstance(user_data, dict):
            user_data = pd.DataFrame([user_data])
        
        # Select only numeric features that were used in training
        numeric_features = user_data.select_dtypes(include=[np.number])
        
        # Predict cluster
        cluster = self.kmeans.predict(numeric_features)
        return cluster[0]
    
    def save_model(self, filepath):
        """Save the trained clustering model"""
        model_data = {
            'kmeans': self.kmeans,
            'pca': self.pca,
            'n_clusters': self.n_clusters,
            'feature_names': self.feature_names
        }
        joblib.dump(model_data, filepath)
        print(f"Model saved to {filepath}")
    
    def load_model(self, filepath):
        """Load a trained clustering model"""
        model_data = joblib.load(filepath)
        self.kmeans = model_data['kmeans']
        self.pca = model_data['pca']
        self.n_clusters = model_data['n_clusters']
        self.feature_names = model_data['feature_names']
        print(f"Model loaded from {filepath}")
