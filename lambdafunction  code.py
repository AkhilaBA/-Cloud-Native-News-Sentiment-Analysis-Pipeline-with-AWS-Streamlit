
import os
import json
import requests
import boto3
import psycopg2
from datetime import datetime

# Environment variables
news_api_key = os.environ.get('NEWS_API_KEY')
s3_bucket = 'S3 Bucket name'
rds_host = os.environ['RDS_HOST']
rds_user = os.environ['RDS_USER']
rds_password = os.environ['RDS_PASSWORD']
rds_port = os.environ.get('RDS_PORT', 5432)
db_name = "database name"
table_name = "table name"

def get_news():
    url = f' api url {news_api_key}'
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Failed to fetch news: {response.status_code} {response.text}")

def upload_to_s3(data):
    s3 = boto3.client('s3')
    s3_file_key = f'folder name/news_{datetime.utcnow().strftime("%Y-%m-%d_%H-%M-%S")}.json'
    s3.put_object(
        Bucket=s3_bucket,
        Key=s3_file_key,
        Body=json.dumps(data),
        ContentType='application/json'
    )
    print(f"File uploaded to s3://{s3_bucket}/{s3_file_key}")

def ensure_table_exists():
    conn = psycopg2.connect(
        host=rds_host,
        user=rds_user,
        password=rds_password,
        port=rds_port,
        database=db_name
    )
    cur = conn.cursor()
    create_table_query = f'''
    CREATE TABLE IF NOT EXISTS {table_name} (
        id SERIAL PRIMARY KEY,
        source_id VARCHAR(100),
        source_name VARCHAR(255),
        author TEXT,
        title TEXT,
        description TEXT,
        url TEXT,
        url_to_image TEXT,
        published_at TIMESTAMP,
        content TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        sentiment_score FLOAT
    );
    '''
    cur.execute(create_table_query)
    conn.commit()
    print(f"Table '{table_name}' ensured.")
    cur.close()
    conn.close()

def insert_articles_to_rds(articles):
    conn = psycopg2.connect(
        host=rds_host,
        user=rds_user,
        password=rds_password,
        port=rds_port,
        database=db_name
    )
    cur = conn.cursor()
    insert_query = f'''
    INSERT INTO {table_name} (
        source_id, source_name, author, title, description, url, url_to_image, published_at, content, sentiment_score
    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, NULL)
    '''
    for article in articles:
        source = article.get('source', {})
        source_id = source.get('id')
        source_name = source.get('name')
        author = article.get('author')
        title = article.get('title')
        description = article.get('description')
        url = article.get('url')
        url_to_image = article.get('urlToImage')
        content = article.get('content')
        published_at = article.get('publishedAt')

        try:
            published_at_dt = datetime.fromisoformat(published_at.replace('Z', '+00:00')) if published_at else None
        except:
            published_at_dt = None

        cur.execute(insert_query, (
            source_id, source_name, author, title, description,
            url, url_to_image, published_at_dt, content
        ))

    conn.commit()
    print(f"{len(articles)} articles inserted into {table_name}")
    cur.close()
    conn.close()

def lambda_handler(event, context):
    try:
        
        news_data = get_news()
        upload_to_s3(news_data)

        
        ensure_table_exists()

      
        articles = news_data.get("articles", [])
        if not articles:
            print("No articles found.")
            return {"statusCode": 204, "body": "No articles found in API response."}

        insert_articles_to_rds(articles)

        return {
            "statusCode": 200,
            "body": "News uploaded to S3 and inserted into PostgreSQL table"
        }

    except Exception as e:
        print(f"ERROR: {e}")
        return {
            "statusCode": 500,
            "body": f"Error occurred: {str(e)}"
        }
