FROM appsvc/python:3.6_1901092346
MAINTAINER shai
WORKDIR /home/site/wwwroot
RUN apt-get install gnupg --assume-yes
RUN curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add -
RUN curl https://packages.microsoft.com/config/debian/9/prod.list > /etc/apt/sources.list.d/mssql-release.list
RUN apt-get install apt-transport-https --assume-yes
RUN apt-get update
RUN apt-get install gcc g++ unixodbc unixodbc-dev --assume-yes
RUN ACCEPT_EULA=Y apt-get install msodbcsql17
RUN pip install pyodbc
RUN odbcinst -j
RUN odbcinst -q -d -n "ODBC Driver 17 for SQL Server"
COPY . .
RUN pip install -r requirements.txt