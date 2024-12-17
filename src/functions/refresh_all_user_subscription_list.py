from google.cloud import bigquery

def refresh_all_user_subscription_list():
    client = bigquery.Client()

    
    print("refresh_all_user_subscription_list")
