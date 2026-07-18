import os
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from scripts.generate_data import generate_courses_csv

class CourseRecommender:
    def __init__(self, csv_path: str = "data/courses.csv"):
        self.csv_path = csv_path
        self.df = None
        self.vectorizer = TfidfVectorizer(stop_words='english')
        self.tfidf_matrix = None
        self.cosine_sim = None
        self.load_data()

    def load_data(self):
        """
        Loads course data from CSV. If it does not exist, generates it first.
        Composes content profiles by merging Title and Description.
        """
        try:
            if not os.path.exists(self.csv_path):
                print(f"Data file {self.csv_path} not found. Triggering automatic data generation...")
                generate_courses_csv(self.csv_path)

            self.df = pd.read_csv(self.csv_path)
            
            # Ensure all expected columns exist defensively
            for col in ['Duration', 'Image_URL', 'Mini_Game_Question', 'Mini_Game_Answer', 'Mini_Game_Options']:
                if col not in self.df.columns:
                    self.df[col] = ''

            # Data cleansing & text profile creation
            self.df['Course_ID'] = self.df['Course_ID'].astype(str)
            self.df['Title'] = self.df['Title'].fillna('').astype(str)
            self.df['Description'] = self.df['Description'].fillna('').astype(str)
            self.df['text_profile'] = self.df['Title'] + " " + self.df['Description']
            self.df['Level_Number'] = pd.to_numeric(self.df['Level_Number']).fillna(1).astype(int)
            self.df['XP_Reward'] = pd.to_numeric(self.df['XP_Reward']).fillna(100).astype(int)
            self.df['Video_URL'] = self.df['Video_URL'].fillna('').astype(str)
            self.df['Mini_Game_Type'] = self.df['Mini_Game_Type'].fillna('').astype(str)
            self.df['Mini_Game_Question'] = self.df['Mini_Game_Question'].fillna('').astype(str)
            self.df['Mini_Game_Answer'] = self.df['Mini_Game_Answer'].fillna('').astype(str)
            self.df['Mini_Game_Options'] = self.df['Mini_Game_Options'].fillna('').astype(str)
            self.df['Duration'] = self.df['Duration'].fillna('').astype(str)
            self.df['Image_URL'] = self.df['Image_URL'].fillna('').astype(str)
            
            # TF-IDF vectorization and cosine similarity
            self.tfidf_matrix = self.vectorizer.fit_transform(self.df['text_profile'])
            self.cosine_sim = cosine_similarity(self.tfidf_matrix, self.tfidf_matrix)
        except Exception as e:
            print(f"Error loading and vectorizing data: {e}")
            raise

    def _convert_numpy_types(self, item: dict) -> dict:
        """
        Converts NumPy numeric data types into native Python types
        to ensure JSON serialization compatibility.
        """
        import numpy as np
        converted = {}
        for k, v in item.items():
            if isinstance(v, (np.float32, np.float64)):
                converted[k] = float(v)
            elif isinstance(v, (np.int32, np.int64)):
                converted[k] = int(v)
            elif isinstance(v, float) and np.isnan(v):
                converted[k] = None
            else:
                converted[k] = v
        return converted

    def get_popular_courses(self, category: str = None, top_n: int = 5) -> list:
        """
        Returns the top N trending courses (sorted by enrollment count and rating)
        as a fallback to solve the Cold-Start problem.
        """
        try:
            if self.df is None or self.df.empty:
                return []
                
            df_filtered = self.df
            if category:
                # Case-insensitive category match
                df_filtered = self.df[self.df['Category'].str.lower() == category.lower()]
                
            # If filtering resulted in nothing, revert to all
            if df_filtered.empty:
                df_filtered = self.df
                
            # Sort by Enrollment_Count desc, then Avg_Rating desc
            popular = df_filtered.sort_values(by=['Enrollment_Count', 'Avg_Rating'], ascending=False)
            results = popular.head(top_n).to_dict(orient='records')
            
            converted_results = []
            for item in results:
                item['match_percentage'] = None
                converted_results.append(self._convert_numpy_types(item))
                
            return converted_results
        except Exception as e:
            print(f"Error fetching popular courses: {e}")
            return []

    def get_content_recommendations(self, course_title: str, top_n: int = 5) -> list:
        """
        Retrieves top N content-based recommendations based on TF-IDF profile similarity.
        Maps cosine similarity [0, 1] to [0, 100] for match_percentage.
        Returns None if course title is not found.
        """
        if self.df is None or self.df.empty:
            raise ValueError("Course dataset is empty or not loaded.")

        # Normalize lookup title
        query = str(course_title).lower().strip()
        normalized_titles = self.df['Title'].str.lower().str.strip()
        matched_idx_list = self.df[normalized_titles == query].index
        
        # If no exact match, try substring matching
        if len(matched_idx_list) == 0:
            substring_matches = self.df[normalized_titles.str.contains(query, case=False, na=False, regex=False)]
            if not substring_matches.empty:
                idx = substring_matches.index[0]
                actual_title = self.df.loc[idx, 'Title']
                print(f"Exact match for '{course_title}' not found. Using closest match: '{actual_title}'")
            else:
                print(f"Course title '{course_title}' not found in the dataset.")
                return None
        else:
            idx = matched_idx_list[0]
            actual_title = self.df.loc[idx, 'Title']

        try:
            # Extract similarity scores for the matched course
            sim_scores = list(enumerate(self.cosine_sim[idx]))
            
            # Sort based on similarity score (index 1) descending
            sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
            
            recommendations = []
            for i, score in sim_scores:
                # Exclude the queried course itself
                if i == idx:
                    continue
                if len(recommendations) >= top_n:
                    break
                    
                course_info = self.df.iloc[i].to_dict()
                
                # Map cosine similarity (0 to 1) to match percentage (0 to 100)
                clamped_score = max(0.0, min(1.0, float(score)))
                course_info['match_percentage'] = round(clamped_score * 100, 1)
                
                # Convert NumPy types
                course_info = self._convert_numpy_types(course_info)
                recommendations.append(course_info)
                
            return recommendations
        except Exception as e:
            print(f"Error calculating content recommendations: {e}")
            raise

    def get_course_by_title(self, course_title: str) -> dict:
        """
        Retrieves details of a single course by its title (exact or substring).
        """
        if self.df is None or self.df.empty:
            raise ValueError("Course dataset is empty or not loaded.")

        query = str(course_title).lower().strip()
        normalized_titles = self.df['Title'].str.lower().str.strip()
        matched_idx_list = self.df[normalized_titles == query].index
        
        if len(matched_idx_list) == 0:
            substring_matches = self.df[normalized_titles.str.contains(query, case=False, na=False, regex=False)]
            if not substring_matches.empty:
                idx = substring_matches.index[0]
            else:
                print(f"Course title '{course_title}' not found in the dataset.")
                return None
        else:
            idx = matched_idx_list[0]
            
        course_info = self.df.iloc[idx].to_dict()
        course_info['match_percentage'] = None
        return self._convert_numpy_types(course_info)
