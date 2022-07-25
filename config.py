class LocalConfig:
    # Database
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:password@localhost/web_form'
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
