package com.tomato.geoclock;

import android.view.View;
import android.widget.Button;

public class Model {
    boolean toggle = false; // toggler for sending info
    String name = ""; // phone name
    Double latitude = 0.0, longitude = 0.0; // will hold gps location
    int delay = 0;

    public int getDelay() { return delay; }

    public void setDelay(int delay) { this.delay = delay; }

    public boolean isToggle() {
        return toggle;
    }

    public void setToggle(Button b) {
        if(name.equalsIgnoreCase("")) return; // we don't want to connect to the server without a name being set for the phone
        toggle = !toggle;
        b.setText(""+toggle);
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public Double getLatitude() {
        return latitude;
    }

    public void setLatitude(Double latitude) {
        this.latitude = latitude;
    }

    public Double getLongitude() {
        return longitude;
    }

    public void setLongitude(Double longitude) {
        this.longitude = longitude;
    }
}
