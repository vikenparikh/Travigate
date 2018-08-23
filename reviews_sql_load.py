import xlrd
import pymysql

# Open the workbook and define the worksheet
book = xlrd.open_workbook("C:\\Users\\Viken\\Desktop\\Memories1\\BE project\\Commit1\\BE Project Final\\reviews.xlsx")
sheet = book.sheet_by_name("reviews")

# Establish a MySQL connection
database = pymysql.connect (host="localhost", user = "root", passwd = "", db = "travigate",charset="utf8")


# Get the cursor, which is used to traverse the database, line by line
cursor = database.cursor()

# Create the INSERT INTO sql query
query = """INSERT INTO reviews (id, username, type, taObjectCity, taObject, rating, helpfulness, total_points, date, title, text, taObjectUrl) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""

# Create a For loop to iterate through each row in the XLS file, starting at row 2 to skip the headers
for r in range(1, sheet.nrows):
    id	= sheet.cell(r,0).value
    username	= sheet.cell(r,1).value
    type = sheet.cell(r,2).value
    taObjectCity = sheet.cell(r,3).value
    taObject = sheet.cell(r,4).value
    rating	= sheet.cell(r,5).value
    helpfulness = sheet.cell(r,6).value
    total_points = sheet.cell(r,7).value
    date = sheet.cell(r,8).value
    title	 = sheet.cell(r,9).value
    text = sheet.cell(r,10).value
    taObjectUrl = sheet.cell(r,11).value
    	# Assign values from each row
    values = (id, username, type, taObjectCity, taObject, rating, helpfulness, total_points, date, title, text, taObjectUrl)
		# Execute sql Query
    cursor.execute(query, values)

# Close the cursor
cursor.close()

# Commit the transaction
database.commit()

# Close the database connection
database.close()