import xlrd
import pymysql
import pandas as pd
# Open the workbook and define the worksheet
book = xlrd.open_workbook("C:\\Users\\Viken\\Desktop\\Memories1\\BE project\\Commit1\\BE Project Final\\users.xlsx")
sheet = book.sheet_by_name("users_full_cleaned")

# Establish a MySQL connection
database = pymysql.connect (host="localhost", user = "root", passwd = "", db = "travigate")

# Get the cursor, which is used to traverse the database, line by line
cursor = database.cursor()

# Create the INSERT INTO sql query
query = """INSERT INTO user (username, password, ageRange, 	gender, numHotelsReviews, numRestReviews, numAttractReviews, num1irstToReview, numRatings, numPhotos, num1orumPosts, numArticles, numCitiesBeen, totalPoints, contribLevel, numHelp1ulVotes, reviewerBadge, travelStyle) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""

# Create a For loop to iterate through each row in the XLS file, starting at row 2 to skip the headers
for r in range(1, sheet.nrows):
    username	= sheet.cell(r,0).value
    password	= sheet.cell(r,1).value
    ageRange = sheet.cell(r,2).value
    gender = sheet.cell(r,3).value
    numHotelsReviews = sheet.cell(r,4).value
    numRestReviews	= sheet.cell(r,5).value
    numAttractReviews = sheet.cell(r,6).value
    num1irstToReview = sheet.cell(r,7).value
    numRatings = sheet.cell(r,8).value
    numPhotos	 = sheet.cell(r,9).value
    num1orumPosts = sheet.cell(r,10).value
    numArticles = sheet.cell(r,11).value
    numCitiesBeen = sheet.cell(r,12).value
    totalPoints = sheet.cell(r,13).value
    contribLevel	= sheet.cell(r,14).value
    numHelp1ulVotes	= sheet.cell(r,15).value
    reviewerBadge	= sheet.cell(r,16).value
    travelStyle	= sheet.cell(r,17).value
    	# Assign values from each row
    values = (username, password, ageRange, gender, numHotelsReviews, numRestReviews, numAttractReviews, num1irstToReview, numRatings, numPhotos, num1orumPosts, numArticles, numCitiesBeen, totalPoints, contribLevel, numHelp1ulVotes, reviewerBadge, travelStyle)
		# Execute sql Query
    cursor.execute(query, values)

# Close the cursor
cursor.close()

# Commit the transaction
database.commit()

# Close the database connection
database.close()




#database = pymysql.connect (host="localhost", user = "root", passwd = "", db = "travigate")
#df_mysql = pd.read_sql('Select * from user;', con=database)    
#print( 'loaded dataframe from MySQL. records:', len(df_mysql))
