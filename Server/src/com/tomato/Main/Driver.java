package com.tomato.Main;

import java.net.*;
import java.io.*;
import java.sql.*;

public class Driver {
	// In order for this to compile properly, the latest version of sqlite-jdbc jar needs to be added to the build path
    public static void main(String[] args) throws IOException {
    	int portNumber = 5665;
    	
    	try {
    		ServerSocket server = new ServerSocket(portNumber);
    		while(true) {
    			Socket client = server.accept();
    			Runnable handler = new ConnectionHandler(client);
    			new Thread(handler).start();
    		}
    	}catch(Exception e) {
    		System.out.println("Exception caught when trying to listen on port " + portNumber + " or listening for a connection");
    		e.printStackTrace();
    	}
    }
}

class ConnectionHandler implements Runnable{
	Socket client = null;
	final String user = "username";
	final String pass = "password";
	final String filename = "database.db";
	public void DBEntry(String testName, String testLat, String testLong) throws SQLException {
		 Connection conn = null;
		 Statement stmt = null;
		 //open connection to the file
		 conn = DriverManager.getConnection("jdbc:sqlite:"+filename, "", "");
		 if (conn != null) {
			 DatabaseMetaData meta = conn.getMetaData();
	         System.out.println("The driver name is " + meta.getDriverName());
	         stmt = conn.createStatement();
	         String q1 = "INSERT or ignore into NMPOOL2485Location(UName, Latitude, Longitude) VALUES('"+testName+"','"+testLat+"','"+testLong+"')";
	         String q2 = "update NMPOOL2485Location set Latitude = '"+testLat+"', Longitude = '"+testLong+"' where Uname = '"+testName+"'";
	         int execute = stmt.executeUpdate(q1);
	         System.out.println(execute);
	         execute = stmt.executeUpdate(q2);
	         System.out.println(execute);
	         conn.close();
		 }
	}
	public ConnectionHandler(Socket client) {
		this.client = client;
	}
	
	public void run() {
		try {
			BufferedReader reader = new BufferedReader(new InputStreamReader(client.getInputStream()));
			String input = reader.readLine();
			String[] details = input.split("/");
			if(details.length == 3) {
				DBEntry(details[0], details[1], details[2]);
			}
			for(String n : details) System.out.print(n+ ", ");
			System.out.println();
		} catch (IOException | SQLException e) {
			e.printStackTrace();
		}
	}
}