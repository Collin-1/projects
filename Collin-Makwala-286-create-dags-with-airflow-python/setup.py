from setuptools import setup

setup(
    name="dags",
    version="0.0.1",
    description="Dags to get pr revies and send email",
    long_description="Grabs all the open pull requests that exist on all the github repos you have access to and store them in a database. For each pull request, it gets the timestamp of the latest review and store that in the database. It Sends an email to you that shows the top 5 PRs that need attention in order of priority.",
    author="Collin Makwala",
    author_email="collinmakwala@gmail.com",
    license="Open Source",
    url="https://github.com/Umuzi-org/Collin-Makwala-286-dags-with-airflow-python.git",
    packages=["dags"],
    zip_safe=False,
)