package com.tomato.geoclock;

import androidx.appcompat.app.AppCompatActivity;
import androidx.core.app.ActivityCompat;

import android.Manifest;
import android.content.Context;
import android.content.pm.PackageManager;
import android.location.Location;
import android.location.LocationListener;
import android.location.LocationManager;
import android.location.LocationProvider;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.TextView;
import com.google.android.material.textfield.TextInputLayout;

public class MainActivity extends AppCompatActivity {
    Model model;
    TextView Lat;
    TextView Long;
    Button send;
    TextInputLayout name; // confirms name
    LocationManager manager; // location manager
    LocationProvider provider; // will be use to set the location provider to gps for the manager
    LocationListener listener;
    Runnable connection;
    Thread thread;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        model = new Model();

//        final int delay = 1000 * 60 * 5; // 5 min delay
        final int delay0 = 10000; // 10 sec delay for testing

        model.setDelay(delay0);
        setContentView(R.layout.activity_main);
        connection = new Connection(model);
        thread = new Thread(connection);
        thread.start();

        Lat = findViewById(R.id.lat);
        Long = findViewById(R.id.Longitude);
        name = findViewById(R.id.name);
        send = findViewById(R.id.button);

        manager = (LocationManager) this.getSystemService(Context.LOCATION_SERVICE);
        provider = manager.getProvider(LocationManager.GPS_PROVIDER);

        listener = new LocationListener() { // will be used for grabbing location and updating display
            public void onLocationChanged(Location location) {
                model.setLatitude(location.getLatitude());
                model.setLongitude(location.getLongitude());
                Lat.setText("" + location.getLatitude());
                Long.setText("" + location.getLongitude());
            }

            public void onStatusChanged(String provider, int status, Bundle extras) {
            }

            public void onProviderEnabled(String provider) {
            }

            public void onProviderDisabled(String provider) {
            }
        };
        if (ActivityCompat.checkSelfPermission(this, Manifest.permission.ACCESS_FINE_LOCATION) != PackageManager.PERMISSION_GRANTED && ActivityCompat.checkSelfPermission(this, Manifest.permission.ACCESS_COARSE_LOCATION) != PackageManager.PERMISSION_GRANTED) {
            // TODO: Consider calling
            //    ActivityCompat#requestPermissions
            // here to request the missing permissions, and then overriding
            //   public void onRequestPermissionsResult(int requestCode, String[] permissions,
            //                                          int[] grantResults)
            // to handle the case where the user grants the permission. See the documentation
            // for ActivityCompat#requestPermissions for more details.
            return;
        }
        manager.requestLocationUpdates(LocationManager.GPS_PROVIDER, model.getDelay(), 10, listener); // we add the listener to the manager and set the delay as well as the minimum distance
    }

    protected void onStop() {
        super.onStop();
        manager.removeUpdates(listener);
        try {
            thread.join();
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
    }

    public void clicked(View v){
        switch(v.getId()){
            case R.id.button:
                model.setToggle(send);
                break;
            case R.id.button2:
                model.setName(name.getEditText().getText().toString());
                break;
        }
    }

}
