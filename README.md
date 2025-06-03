# 📰 Cloud-Native News Sentiment Dashboard

This project automates real-time news sentiment analysis using AWS services and visualizes the results through a Streamlit dashboard hosted on ECS Fargate.

## 🔧 Technologies Used

- AWS Lambda  
- Amazon EventBridge  
- Amazon S3  
- Amazon RDS (PostgreSQL)  
- Docker & Amazon ECR  
- Amazon ECS (Fargate)  
- Streamlit  
- TextBlob (for sentiment analysis)

## 🔄 Data Pipeline Flow

1. **AWS EventBridge** triggers Lambda every 5 minutes.
2. **Lambda** fetches U.S. news headlines from the News API.
3. Performs **sentiment analysis** using `TextBlob`.
4. Stores raw JSON in **Amazon S3**.
5. Stores cleaned, labeled data in **Amazon RDS (PostgreSQL)**.
6. A **Streamlit dashboard**, containerized using Docker, fetches sentiment data from RDS.
7. Docker image is pushed to **Amazon ECR** and deployed to **ECS Fargate**.
8. Dashboard is accessible through a **public IP**.

---

## 🧠 Sentiment Score Interpretation

Sentiment is calculated using TextBlob's polarity:

- Positive: `score > 0.1`  
- Neutral: `-0.1 ≤ score ≤ 0.1`  
- Negative: `score < -0.1`

Example Output:

| Headline                                | Sentiment Score | Label     |
|-----------------------------------------|------------------|-----------|
| "Stock market rebounds sharply"         | 0.76             | Positive  |
| "Inflation remains flat"                | 0.04             | Neutral   |
| "Violence erupts in capital"            | -0.62            | Negative  |

---


## 📂 Project Files

- [lambdacode.py](lambdacode.py) — Fetches news from the News API and saves data to both S3 and RDS.
- [streamlit.py](streamlit.py) — Streamlit dashboard code that reads from RDS and displays sentiment data.
- [dockerfile](dockerfile) —  Builds the Docker image for the Streamlit app.
- [requirement.txt](requirement.txt) — This requirements.txt file lists the Python packages



## ⚙️ Setup Instructions

# 🔹 1. Lambda Functions

- **Lambda 1 (Raw Ingestor)**:
  - Fetches articles from NewsAPI.
  - Saves raw JSON data to S3.

- **Lambda 2 (Processor)**:
  - Reads from S3.
  - Cleans and analyzes sentiment.
  - Inserts records into RDS PostgreSQL.

# 🔹 2. PostgreSQL on RDS

- Create an RDS PostgreSQL instance.
- Note the **endpoint**, **username**, and **password**.
- Use SQL commands via Python (psycopg2) to create tables inside Lambda.

# 🔹 3. Sentiment Analysis

- Performed in Lambda using `TextBlob`.
- Sentiment classification based on polarity:
  - Positive: `> 0.1`
  - Neutral: `-0.1 ≤ score ≤ 0.1`
  - Negative: `< -0.1`

# 🔹 4. Streamlit Dashboard

- Read data from RDS using `psycopg2` or `SQLAlchemy`.
- Display:
  - News headlines
  - Sentiment labels
  - Pie/Bar charts
  - Date filters

# 🔹 5. Dockerization

- Build Docker image:

  ```bash
  docker build -t streamlit-news-dashboard .
  
- Run locally to test:

  ```bash
  docker run -p port:port streamlit-news-dashboard

# 🔹 6. Push to ECR

Tag and push your image:

```bash
aws ecr create-repository --repository-name streamlit-news
docker tag streamlit-news-dashboard:latest <your-ecr-uri>
docker push <your-ecr-uri>

# 🔹 7. Deploy to ECS Fargate

  Create ECS Task Definition with ECR image.
  
  Set up ECS Service (Fargate) with public subnet.
  
  Map port [your own port].
  
  Access dashboard via public IP.







