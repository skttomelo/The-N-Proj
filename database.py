import sqlite3

conn = sqlite3.connect('database.db')

c = conn.cursor()
c.execute('''create table NMPOOL2485Location(
    UName text not null unique,
    Latitude text not null,
    Longitude text not null)''')

conn.commit()


'''
create table NMPOOL2485.Location(
    UName varchar(255) not null unique identity(1,1),
    Latitude varchar(255) not null,
    Longitude varchar(255) not null
);

go

CREATE PROCEDURE InsertName
(
  @uname varchar(255),
  @Lat varchar(255),
  @Lon varchar(255)
)
AS
IF EXISTS(SELECT 'True' FROM NMPOOL2485.Location WHERE UName = @uname)
BEGIN
  --Record exist
  update NMPOOL2485.Location
  set Latitude = @Lat, Longitude = @Lon
  where Uname = @uname;
END
ELSE
BEGIN
  --Record does not exist
  INSERT into NMPOOL2485.Location(UName, Latitude, Longitude) VALUES(@uname, @Lat, @Lon);
END

go
'''