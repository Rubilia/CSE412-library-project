import os

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "supersecretkey")
    DB_DSN = "postgresql://cse412db_owner:2Qqcbp9CvasX@ep-quiet-star-a6r8acx0.us-west-2.aws.neon.tech/cse412db?sslmode=require"
