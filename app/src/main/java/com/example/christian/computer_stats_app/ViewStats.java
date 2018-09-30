package com.example.christian.computer_stats_app;

import android.app.ListActivity;
import android.app.ProgressDialog;
import android.content.Intent;
import android.os.AsyncTask;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.util.Log;
import android.widget.ListAdapter;
import android.widget.ListView;
import android.widget.SimpleAdapter;
import android.widget.TextView;

import org.apache.http.NameValuePair;
import org.apache.http.message.BasicNameValuePair;
import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.net.URI;
import java.net.URISyntaxException;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;

public class ViewStats extends AppCompatActivity {

    TextView cpuPercent;
    TextView cpuMaxPercent;
    String cid;
    int recievedCpuPercent;
    int recievedCpuMaxPercent;

    // Progress Dialog
    private ProgressDialog pDialog;

    // Creating JSON Parser object
    JSONParser jParser = new JSONParser();

    ArrayList<HashMap<String, String>> computerStatsList;

    // url to get all cpu stats
    private static URI url_computer_stats;

    static {
        try {
            url_computer_stats = new URI("http", "192.168.1.87:8888", "/computer_stats_connector/get_computer_stats.php", null, null);
        } catch (URISyntaxException e) {
            e.printStackTrace();
        }
    }

    // JSON Node names
    private static final String TAG_SUCCESS = "success";
    private static final String TAG_CID = "cid";
    private static final String TAG_CPU_PERCENT = "cpu_percent";
    private static final String TAG_CPU_MAX_PERCENT = "cpu_max_percent";

    // products JSONArray
    JSONArray computerStats = null;

    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_view_stats);

        // getting id from intent
        Intent i = getIntent();

        // getting id from intent
        cid = i.getStringExtra(TAG_CID);

        Thread thread = new Thread() {
            @Override
            public void run() {
                try {
                    while (!isInterrupted()) {
                        Thread.sleep(1000);
                        runOnUiThread(new Runnable() {
                            @Override
                            public void run() {
                                new LoadCpuStats().execute();
                                cpuPercent = (TextView) findViewById(R.id.cpu_percent);
                                cpuMaxPercent = (TextView) findViewById(R.id.max_cpu_percent);

                                cpuPercent.setText(recievedCpuPercent+"%");
                                cpuMaxPercent.setText(recievedCpuMaxPercent+"%");
                            }
                        });
                    }
                } catch (InterruptedException e) {
                }
            }
        };

        thread.start();
    }

    /**
     * Background Async Task to Load all product by making HTTP Request
     * */
    class LoadCpuStats extends AsyncTask<String, String, String> {

        /**
         * getting All products from url
         * */
        protected String doInBackground(String... args) {
            // Building Parameters
            List<NameValuePair> params = new ArrayList<NameValuePair>();
            params.add(new BasicNameValuePair("cid", cid));
            // getting JSON string from URL
            JSONObject json = jParser.makeHttpRequest(url_computer_stats, "GET", params);

            // Check your log cat for JSON response
            Log.d("Computer Stats: ", json.toString());

            try {
                // Checking for SUCCESS TAG
                int success = json.getInt(TAG_SUCCESS);
                if (success == 1) {
                    // cpu stats found
                    recievedCpuPercent = (int) Math.round(Double.parseDouble(json.getString(TAG_CPU_PERCENT)));
                    recievedCpuMaxPercent = (int) Math.round(Double.parseDouble(json.getString(TAG_CPU_MAX_PERCENT)));
                }
            } catch (JSONException e) {
                e.printStackTrace();
            }
            return null;
        }

        /**
         * After completing background task Dismiss the progress dialog
         * **/
        protected void onPostExecute(String file_url) {
            // updating UI from Background Thread
            runOnUiThread(new Runnable() {
                public void run() {
                }
            });

        }

    }
}
