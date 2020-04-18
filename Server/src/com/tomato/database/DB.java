package com.tomato.database;

//import java.io.File;
//import java.io.IOException;
import java.sql.Connection;
import java.sql.DatabaseMetaData;
import java.sql.DriverManager;
import java.sql.SQLException;
import java.sql.Statement;

public class DB {
	public static void main(String[] args) throws SQLException {
		final String user = "username";
		final String pass = "password";
		final String filename = "database.db";
//		File database = new File(filename);
//		try {
//			database.createNewFile();
//		} catch (IOException e) {
//			e.printStackTrace();
//		}
	   Connection conn = null;
	   Statement stmt = null;
	   //open connection to the file
	   conn = DriverManager.getConnection("jdbc:sqlite:"+filename, "", "");
	   if (conn != null) {
           DatabaseMetaData meta = conn.getMetaData();
           System.out.println("The driver name is " + meta.getDriverName());
           stmt = conn.createStatement();
           String testName = "Nicholas";
           String testLat = "22.22";
           String testLong = "22.22";
           String q1 = "INSERT or ignore into NMPOOL2485Location(UName, Latitude, Longitude) VALUES('"+testName+"','"+testLat+"','"+testLong+"')";
           String q2 = "update NMPOOL2485Location set Latitude = '"+testLat+"', Longitude = '"+testLong+"' where Uname = '"+testName+"'";
           int execute = stmt.executeUpdate(q1);
           System.out.println(execute);
           execute = stmt.executeUpdate(q2);
           System.out.println(execute);
           conn.close();
       }
	}
}
