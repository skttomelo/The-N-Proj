package com.tomato.geoclock;

import java.io.PrintWriter;
import java.net.Socket;

public class Connection extends Thread implements Runnable{
    private Model model;
    private String ip = "172.28.237.126"; // this will be used to connect to the server that will take gps data
    private int port = 5665; // port of the address that we want to connect to

    public Connection(Model m){
        model = m;
    }

    public void run() {
        while(true){
            if(model.isToggle() == true){
                try (
                    Socket client = new Socket(ip, port);
                    PrintWriter out = new PrintWriter(client.getOutputStream(), true);
                ) {
                    out.println(model.getName()+"/"+model.getLatitude()+"/"+model.getLatitude());
                }catch(Exception e){
                    e.printStackTrace();
                }
            }

            try {
                this.sleep(model.getDelay());
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
        }
    }
}
