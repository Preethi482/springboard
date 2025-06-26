/* Welcome to the SQL mini project. You will carry out this project partly in
the PHPMyAdmin interface, and partly in Jupyter via a Python connection.

This is Tier 1 of the case study, which means that there'll be more guidance for you about how to 
setup your local SQLite connection in PART 2 of the case study. 

The questions in the case study are exactly the same as with Tier 2. 

PART 1: PHPMyAdmin
You will complete questions 1-9 below in the PHPMyAdmin interface. 
Log in by pasting the following URL into your browser, and
using the following Username and Password:

URL: https://sql.springboard.com/
Username: student
Password: learn_sql@springboard

The data you need is in the "country_club" database. This database
contains 3 tables:
    i) the "Bookings" table,
    ii) the "Facilities" table, and
    iii) the "Members" table.

In this case study, you'll be asked a series of questions. You can
solve them using the platform, but for the final deliverable,
paste the code for each solution into this script, and upload it
to your GitHub.

Before starting with the questions, feel free to take your time,
exploring the data, and getting acquainted with the 3 tables. */


/* QUESTIONS 
/* Q1: Some of the facilities charge a fee to members, but some do not.
Write a SQL query to produce a list of the names of the facilities that do. */
SELECT name
FROM Facilities
WHERE membercost > 0;


/* Q2: How many facilities do not charge a fee to members? */

Answer : 4
/* Q3: Write an SQL query to show a list of facilities that charge a fee to members,
where the fee is less than 20% of the facility's monthly maintenance cost.
Return the facid, facility name, member cost, and monthly maintenance of the
facilities in question. */
Answer :
SELECT facid, name, membercost, monthlymaintenance
FROM Facilities
WHERE membercost > 0 
  AND membercost < (0.2 * monthlymaintenance);


/* Q4: Write an SQL query to retrieve the details of facilities with ID 1 and 5.
Try writing the query without using the OR operator. */
SELECT *
FROM Facilities
WHERE facid IN (1, 5);


/* Q5: Produce a list of facilities, with each labelled as
'cheap' or 'expensive', depending on if their monthly maintenance cost is
more than $100. Return the name and monthly maintenance of the facilities
in question. */

Tennis Court 1
200
expensive
Tennis Court 2
200
expensive
Badminton Court
50
cheap
Table Tennis
10
cheap
Massage Room 1
3000
expensive
Massage Room 2
3000
expensive
Squash Court
80
cheap
Snooker Table
15
cheap
Pool Table
15
cheap


/* Q6: You'd like to get the first and last name of the last member(s)
who signed up. Try not to use the LIMIT clause for your solution. */

Answer : Darren
Smith

/* Q7: Produce a list of all members who have used a tennis court.
Include in your output the name of the court, and the name of the member
formatted as a single column. Ensure no duplicate data, and order by
the member name. */

Answer : Tennis Court 1
0
Tennis Court 2
0
/* Q8: Produce a list of bookings on the day of 2012-09-14 which
will cost the member (or guest) more than $30. Remember that guests have
different costs to members (the listed costs are per half-hour 'slot'), and
the guest user's ID is always 0. Include in your output the name of the
facility, the name of the member formatted as a single column, and the cost.
Order by descending cost, and do not use any subqueries. */

Answer ---- 
facility_name
member_name
cost Descending
Massage Room 2
0
320.0
Massage Room 1
0
160.0
Massage Room 1
0
160.0
Massage Room 1
0
160.0
Tennis Court 2
0
150.0
Tennis Court 2
0
75.0
Tennis Court 1
0
75.0
Tennis Court 1
0
75.0
Squash Court
0
70.0
Massage Room 1
0
39.6
Squash Court
0
35.0
Squash Court
0
35.0



/* Q9: This time, produce the same result as in Q8, but using a subquery. */
SELECT facility_name, member_name, cost
FROM (
    SELECT f.name AS facility_name,
           m.firstname || ' ' || m.surname AS member_name,
           (b.slots * 
            CASE 
                WHEN b.memid = 0 THEN f.guestcost
                ELSE f.membercost
            END) AS cost
    FROM Bookings b
    JOIN Facilities f ON b.facid = f.facid
    JOIN Members m ON b.memid = m.memid
    WHERE b.starttime LIKE '2012-09-14%'
) AS booking_costs
WHERE cost > 30
ORDER BY cost DESC;


/* PART 2: SQLite
/* We now want you to jump over to a local instance of the database on your machine. 

Copy and paste the LocalSQLConnection.py script into an empty Jupyter notebook, and run it. 

Make sure that the SQLFiles folder containing thes files is in your working directory, and
that you haven't changed the name of the .db file from 'sqlite\db\pythonsqlite'.

You should see the output from the initial query 'SELECT * FROM FACILITIES'.
Answer"   SQLite version: 2.6.0
2. Query all facilities
   facid             name  membercost  guestcost  initialoutlay  \
0      0   Tennis Court 1         5.0       25.0          10000   
1      1   Tennis Court 2         5.0       25.0           8000   
2      2  Badminton Court         0.0       15.5           4000   
3      3     Table Tennis         0.0        5.0            320   
4      4   Massage Room 1         9.9       80.0           4000   

   monthlymaintenance  
0                 200  
1                 200  
2                  50  
3                  10  
4                3000  
Complete the remaining tasks in the Jupyter interface. If you struggle, feel free to go back
to the PHPMyAdmin interface as and when you need to. 

You'll need to paste your query into value of the 'query1' variable and run the code block again to get an output.
 
QUESTIONS:
/* Q10: Produce a list of facilities with a total revenue less than 1000.
The output of facility name and total revenue, sorted by revenue. Remember
that there's a different cost for guests and members! */

Answer : facility_name
total_revenue Ascending
Table Tennis
180.0
Snooker Table
240.0
Pool Table
270.0


/* Q11: Produce a report of members and who recommended them in alphabetic surname,firstname order */


/* Q12: Find the facilities with their usage by member, but not guests */

Answer 
SELECT f.name AS facility_name,
       COUNT(*) AS usage_count
FROM Bookings b
JOIN Facilities f ON b.facid = f.facid
WHERE b.memid != 0
GROUP BY f.name
ORDER BY usage_count DESC;

facility_name
usage_count Descending
Pool Table
783
Massage Room 1
421
Snooker Table
421
Table Tennis
385
Badminton Court
344
Tennis Court 1
308
Tennis Court 2
276
Squash Court
195
Massage Room 2
27



/* Q13: Find the facilities usage by month, but not guests */
SELECT 
    DATE_FORMAT(b.starttime, '%Y-%m') AS month,
    f.name AS facility_name,
    COUNT(*) AS usage_count
FROM Bookings b
JOIN Facilities f ON b.facid = f.facid
WHERE b.memid != 0
GROUP BY month, f.name
ORDER BY month, f.name;

month
facility_name
usage_count
2012-07
Badminton Court
51
2012-07
Massage Room 1
77
2012-07
Massage Room 2
4
2012-07
Pool Table
103
2012-07
Snooker Table
68
2012-07
Squash Court
23
2012-07
Table Tennis
48
2012-07
Tennis Court 1
65
2012-07
Tennis Court 2
41
2012-08
Badminton Court
132
2012-08
Massage Room 1
153
2012-08
Massage Room 2
9
2012-08
Pool Table
272
2012-08
Snooker Table
154
2012-08
Squash Court
85
2012-08
Table Tennis
143
2012-08
Tennis Court 1
111
2012-08
Tennis Court 2
109
2012-09
Badminton Court
161
2012-09
Massage Room 1
191
2012-09
Massage Room 2
14
2012-09
Pool Table
408
2012-09
Snooker Table
199
2012-09
Squash Court
87
2012-09
Table Tennis
194
2012-09
Tennis Court 1
132
2012-09
Tennis Court 2
126


