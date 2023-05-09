
import pandas as pd
import stats
import numpy as np
import seaborn as sn
import matplotlib.pyplot as plt
from sklearn import preprocessing, metrics
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC
from sklearn import model_selection
def main():
    start = 2021
    end = 2022
    
    ###### ONCE PER DAY ######
    # Save all stats from a range of seasons to a JSON file
    # stats_dict = stats.save_all_reg_stats(start, end)
    ###### ONCE PER DAY ######
    
    # # Load all stats from a JSON file
    # stats_dict = stats.load_from_json('data/2021_2022_regular.json')
    
    # # Parse all players for a given position
    # pos_info = stats.parse_pos_info('data/players_info.json', 'QB')
    
    # # Parse stats for a given position, save to JSON file named {pos}_stats.json
    # qb_stats = stats.parse_pos_stats('data/2021_2022_regular.json', 'QB')
    
    # # Remove players with no stats
    # qb_stats_removed = stats.remove_players_no_stats(qb_stats)
    # stats.save_to_json(qb_stats_removed, 'QB_stats_nan_removed.json')
    
    # # Calculate fantasy scores for a given position
    # qb_stats_removed_calculated = stats.calculate_fpts(qb_stats_removed)
    # stats.save_to_json(qb_stats_removed_calculated, 'QB_stats_with_scores.json')
    
    # # Flatten Stats 
    # flattened_stats = stats.flatten_stats('data/QB_stats_with_scores.json')
    # stats.save_to_json(flattened_stats, 'QB_stats_flattened.json')
    flattened_stats = stats.load_from_json('data/QB_stats_flattened.json')
    data = pd.DataFrame.from_dict(flattened_stats)
    data.fillna(0, inplace=True)

    # Convert objects to floats
    data_T = data.T
    for col in data_T.columns:
        if data_T[col].dtype == 'object':
            data_T[col] = data_T[col].astype('float64')
            
    # print(data.dtypes)
    # print(data_T.dtypes)
    
    # Drop unnecessary columns
    data_T.drop(['pts_ppr', 'pts_half_ppr', 'pts_std', 'rank_std', 'rank_ppr', 'pos_rank_std', 'pos_rank_std', 'pos_rank_ppr', 'pos_rank_half_ppr'], axis=1, inplace=True)
    
    # Create Correlation Matrix
    correlation_matrix = data_T.corr()
    
    # Save Correlation Matrix to JSON file and print
    correlation_matrix['calculated_fpts'].sort_values(ascending=False).to_json('data/correlation_matrix.json')
    # print(correlation_matrix['calculated_fpts'].sort_values(ascending=False))

    # Drop columns with low correlation
    not_correlated = [f'{row}' for row in correlation_matrix['calculated_fpts'].keys() if correlation_matrix['calculated_fpts'][row] < 0.5]
    data_T.drop(not_correlated, axis=1, inplace=True)
    dropped_correlation_matrix = data_T.corr()
    # print(dropped_correlation_matrix['calculated_fpts'].sort_values(ascending=False))
    
    # Save data to CSV and JSON files
    data_T.to_csv('data/qb_model_data.csv') # index=False ???
    # data_T.to_json('data/qb_model_data.json')
    print(data_T.dtypes)
    new_data = pd.read_csv('data/qb_model_data.csv')
    print(new_data.dtypes)   
    # scaler = preprocessing.StandardScaler()
    # scaler.fit(data_T)    
    # features = data_T.drop(['calculated_fpts'], axis=1)
    # fpts = data_T['calculated_fpts']
    # scaled_array = scaler.fit_transform(features, fpts)
    # print(scaled_array)
    # scaled_data = pd.DataFrame(scaled_array, columns=data_T.columns)
    # print(scaled_data.dtypes)
    
    X_train, X_test, y_train, y_test = model_selection.train_test_split(data_T.drop(['calculated_fpts'], axis=1), data_T['calculated_fpts'], test_size=0.2)
    print(X_train.dtypes)
    print(y_train.dtypes)
    # y_train = y_train.astype('float64')
    # X_train = X_train.astype('str')
    # print(y_train.head())
    # print(y_train.dtypes)
    # sn.heatmap(correlation_matrix)
    # plt.show()    
    # r_squared = correlation_matrix[0,1]**2
    # print(r_squared)
    
    # Initialize and fit model to training data
    # model = GaussianNB()
    # model.fit(X_train, y_train)
    # # Use model to predict output based on test data
    # y_pred = model.predict(X_test)
    # print(y_pred)

    #Calculate score and classification report
    # nb_score1 = metrics.accuracy_score(y_test, y_pred)
    # nb_score2 = round(model.score(X_train, y_train) * 100, 2)
    # nb_report = metrics.classification_report(y_test, y_pred)
    # print("Naive Bayes Accuracy: ", nb_score1)
    # print("Classification Report: \n", nb_report)    


if __name__ == '__main__':
    main()



