package com.example.christian.computer_stats_app;

import android.app.ListActivity;
import android.app.ProgressDialog;
import android.content.Intent;
import android.os.AsyncTask;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
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

    TextView tStatusLabel;
    TextView tCpuStatsLabel;
    TextView tCpuPercentLabel;
    TextView tCpuMaxPercentLabel;
    TextView tCpuCountPhysicalLabel;
    TextView tCpuCountLogicalLabel;
    TextView tCpuFrequencyLabel;
    TextView tMemoryStatsLabel;
    TextView tMemoryTotalLabel;
    TextView tMemoryAvailableLabel;
    TextView tMemoryUsedLabel;
    TextView tMemoryPercentLabel;
    TextView tSystemBootTimeLabel;
    TextView tComputerUserLabel;
    TextView tCpuPercent;
    TextView tCpuMaxPercent;
    TextView tCpuCountPhysical;
    TextView tCpuCountLogical;
    TextView tCpuFrequency;
    TextView tMemoryTotal;
    TextView tMemoryAvailable;
    TextView tMemoryUsed;
    TextView tMemoryPercent;
    TextView tSystemBootTime;
    TextView tComputerUser;
    String cid;
    String error;
    int tracking_all_stats;
    int tracking_cpu;
    int tracking_memory;
    int tracking_disk;
    double cpuPercent;
    double cpuMaxPercent;
    int cpuCountPhysical;
    int cpuCountLogical;
    double cpuFrequency;
    double memoryTotal;
    double memoryAvailable;
    double memoryUsed;
    double memoryPercent;
    String systemBootTime;
    String computerUser;

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
    private static final String TAG_TRACKING_ALL_STATS = "tracking_all_stats";
    private static final String TAG_TRACKING_CPU = "tracking_cpu";
    private static final String TAG_TRACKING_MEMORY = "tracking_memory";
    private static final String TAG_TRACKING_DISK = "tracking_disk";
    private static final String TAG_CPU_PERCENT = "cpu_percent";
    private static final String TAG_CPU_MAX_PERCENT = "cpu_max_percent";
    private static final String TAG_CPU_COUNT_PHYSICAL = "cpu_count_physical";
    private static final String TAG_CPU_COUNT_LOGICAL = "cpu_count_logical";
    private static final String TAG_CPU_FREQUENCY = "cpu_frequency";
    private static final String TAG_MEMORY_TOTAL = "memory_total";
    private static final String TAG_MEMORY_AVAILABLE = "memory_available";
    private static final String TAG_MEMORY_USED = "memory_used";
    private static final String TAG_MEMORY_PERCENT = "memory_percent";
    private static final String TAG_SYSTEM_BOOT_TIME = "system_boot_time";
    private static final String TAG_COMPUTER_USER = "computer_user";

    // products JSONArray
    JSONArray computerStats = null;

    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_view_stats);
        setTitle("Computer Stats");

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
                                if (tracking_all_stats == 1) {
                                    tStatusLabel = (TextView) findViewById(R.id.status_label);
                                    tStatusLabel.setVisibility(View.GONE);
                                    tComputerUser = (TextView) findViewById(R.id.computer_user);
                                    tComputerUser.setVisibility(View.VISIBLE);
                                    tComputerUser.setText(computerUser);
                                    tSystemBootTime = (TextView) findViewById(R.id.system_boot_time);
                                    tSystemBootTime.setVisibility(View.VISIBLE);
                                    tSystemBootTime.setText(systemBootTime);
                                    tComputerUserLabel = (TextView) findViewById(R.id.computer_user_label);
                                    tComputerUserLabel.setVisibility(View.VISIBLE);
                                    tSystemBootTimeLabel = (TextView) findViewById(R.id.system_boot_time_label);
                                    tSystemBootTimeLabel.setVisibility(View.VISIBLE);
                                    if (tracking_cpu == 1) {
                                        tCpuStatsLabel = (TextView) findViewById(R.id.cpu_stats_label);
                                        tCpuPercentLabel = (TextView) findViewById(R.id.cpu_percent_label);
                                        tCpuMaxPercentLabel = (TextView) findViewById(R.id.cpu_max_percent_label);
                                        tCpuCountPhysicalLabel = (TextView) findViewById(R.id.cpu_count_physical_label);
                                        tCpuCountLogicalLabel = (TextView) findViewById(R.id.cpu_count_logical_label);
                                        tCpuFrequencyLabel = (TextView) findViewById(R.id.cpu_frequency_label);
                                        tCpuStatsLabel.setVisibility(View.VISIBLE);
                                        tCpuPercentLabel.setVisibility(View.VISIBLE);
                                        tCpuMaxPercentLabel.setVisibility(View.VISIBLE);
                                        tCpuCountPhysicalLabel.setVisibility(View.VISIBLE);
                                        tCpuCountLogicalLabel.setVisibility(View.VISIBLE);
                                        tCpuFrequencyLabel.setVisibility(View.VISIBLE);
                                        tCpuPercent = (TextView) findViewById(R.id.cpu_percent);
                                        tCpuMaxPercent = (TextView) findViewById(R.id.cpu_max_percent);
                                        tCpuCountPhysical = (TextView) findViewById(R.id.cpu_count_physical);
                                        tCpuCountLogical = (TextView) findViewById(R.id.cpu_count_logical);
                                        tCpuFrequency = (TextView) findViewById(R.id.cpu_frequency);
                                        tCpuPercent.setVisibility(View.VISIBLE);
                                        tCpuMaxPercent.setVisibility(View.VISIBLE);
                                        tCpuCountPhysical.setVisibility(View.VISIBLE);
                                        tCpuCountLogical.setVisibility(View.VISIBLE);
                                        tCpuFrequency.setVisibility(View.VISIBLE);
                                        tCpuPercent.setText(cpuPercent+"%");
                                        tCpuMaxPercent.setText(cpuMaxPercent+"%");
                                        tCpuCountPhysical.setText(Integer.toString(cpuCountPhysical));
                                        tCpuCountLogical.setText(Integer.toString(cpuCountLogical));
                                        tCpuFrequency.setText(cpuFrequency+" GHz");
                                    } else {
                                        tCpuStatsLabel = (TextView) findViewById(R.id.cpu_stats_label);
                                        tCpuPercentLabel = (TextView) findViewById(R.id.cpu_percent_label);
                                        tCpuMaxPercentLabel = (TextView) findViewById(R.id.cpu_max_percent_label);
                                        tCpuCountPhysicalLabel = (TextView) findViewById(R.id.cpu_count_physical_label);
                                        tCpuCountLogicalLabel = (TextView) findViewById(R.id.cpu_count_logical_label);
                                        tCpuFrequencyLabel = (TextView) findViewById(R.id.cpu_frequency_label);
                                        tCpuStatsLabel.setVisibility(View.GONE);
                                        tCpuPercentLabel.setVisibility(View.GONE);
                                        tCpuMaxPercentLabel.setVisibility(View.GONE);
                                        tCpuCountPhysicalLabel.setVisibility(View.GONE);
                                        tCpuCountLogicalLabel.setVisibility(View.GONE);
                                        tCpuFrequencyLabel.setVisibility(View.GONE);
                                        tCpuPercent = (TextView) findViewById(R.id.cpu_percent);
                                        tCpuMaxPercent = (TextView) findViewById(R.id.cpu_max_percent);
                                        tCpuCountPhysical = (TextView) findViewById(R.id.cpu_count_physical);
                                        tCpuCountLogical = (TextView) findViewById(R.id.cpu_count_logical);
                                        tCpuFrequency = (TextView) findViewById(R.id.cpu_frequency);
                                        tCpuPercent.setVisibility(View.GONE);
                                        tCpuMaxPercent.setVisibility(View.GONE);
                                        tCpuCountPhysical.setVisibility(View.GONE);
                                        tCpuCountLogical.setVisibility(View.GONE);
                                        tCpuFrequency.setVisibility(View.GONE);
                                    }
                                    if (tracking_memory == 1) {
                                        tMemoryStatsLabel = (TextView) findViewById(R.id.memory_stats_label);
                                        tMemoryTotalLabel = (TextView) findViewById(R.id.memory_total_label);
                                        tMemoryAvailableLabel = (TextView) findViewById(R.id.memory_available_label);
                                        tMemoryUsedLabel = (TextView) findViewById(R.id.memory_used_label);
                                        tMemoryPercentLabel = (TextView) findViewById(R.id.memory_percent_label);
                                        tMemoryStatsLabel.setVisibility(View.VISIBLE);
                                        tMemoryTotalLabel.setVisibility(View.VISIBLE);
                                        tMemoryAvailableLabel.setVisibility(View.VISIBLE);
                                        tMemoryUsedLabel.setVisibility(View.VISIBLE);
                                        tMemoryPercentLabel.setVisibility(View.VISIBLE);
                                        tMemoryTotal = (TextView) findViewById(R.id.memory_total);
                                        tMemoryAvailable = (TextView) findViewById(R.id.memory_available);
                                        tMemoryUsed = (TextView) findViewById(R.id.memory_used);
                                        tMemoryPercent = (TextView) findViewById(R.id.memory_percent);
                                        tMemoryTotal.setVisibility(View.VISIBLE);
                                        tMemoryAvailable.setVisibility(View.VISIBLE);
                                        tMemoryUsed.setVisibility(View.VISIBLE);
                                        tMemoryPercent.setVisibility(View.VISIBLE);
                                        tMemoryTotal.setText(memoryTotal+" GB");
                                        tMemoryAvailable.setText(memoryAvailable+" GB");
                                        tMemoryUsed.setText(memoryUsed+"GB");
                                        tMemoryPercent.setText(memoryPercent+"%");
                                    } else {
                                        tMemoryStatsLabel = (TextView) findViewById(R.id.memory_stats_label);
                                        tMemoryTotalLabel = (TextView) findViewById(R.id.memory_total_label);
                                        tMemoryAvailableLabel = (TextView) findViewById(R.id.memory_available_label);
                                        tMemoryUsedLabel = (TextView) findViewById(R.id.memory_used_label);
                                        tMemoryPercentLabel = (TextView) findViewById(R.id.memory_percent_label);
                                        tMemoryStatsLabel.setVisibility(View.GONE);
                                        tMemoryTotalLabel.setVisibility(View.GONE);
                                        tMemoryAvailableLabel.setVisibility(View.GONE);
                                        tMemoryUsedLabel.setVisibility(View.GONE);
                                        tMemoryPercentLabel.setVisibility(View.GONE);
                                        tMemoryTotal = (TextView) findViewById(R.id.memory_total);
                                        tMemoryAvailable = (TextView) findViewById(R.id.memory_available);
                                        tMemoryUsed = (TextView) findViewById(R.id.memory_used);
                                        tMemoryPercent = (TextView) findViewById(R.id.memory_percent);
                                        tMemoryTotal.setVisibility(View.GONE);
                                        tMemoryAvailable.setVisibility(View.GONE);
                                        tMemoryUsed.setVisibility(View.GONE);
                                        tMemoryPercent.setVisibility(View.GONE);
                                    }
                                } else {
                                    tStatusLabel = (TextView) findViewById(R.id.status_label);
                                    tStatusLabel.setVisibility(View.VISIBLE);
                                    tComputerUser = (TextView) findViewById(R.id.computer_user);
                                    tComputerUser.setVisibility(View.GONE);
                                    tSystemBootTime = (TextView) findViewById(R.id.system_boot_time);
                                    tSystemBootTime.setVisibility(View.GONE);
                                    tComputerUserLabel = (TextView) findViewById(R.id.computer_user_label);
                                    tComputerUserLabel.setVisibility(View.GONE);
                                    tSystemBootTimeLabel = (TextView) findViewById(R.id.system_boot_time_label);
                                    tSystemBootTimeLabel.setVisibility(View.GONE);
                                    tCpuStatsLabel = (TextView) findViewById(R.id.cpu_stats_label);
                                    tCpuPercentLabel = (TextView) findViewById(R.id.cpu_percent_label);
                                    tCpuMaxPercentLabel = (TextView) findViewById(R.id.cpu_max_percent_label);
                                    tCpuCountPhysicalLabel = (TextView) findViewById(R.id.cpu_count_physical_label);
                                    tCpuCountLogicalLabel = (TextView) findViewById(R.id.cpu_count_logical_label);
                                    tCpuFrequencyLabel = (TextView) findViewById(R.id.cpu_frequency_label);
                                    tCpuStatsLabel.setVisibility(View.GONE);
                                    tCpuPercentLabel.setVisibility(View.GONE);
                                    tCpuMaxPercentLabel.setVisibility(View.GONE);
                                    tCpuCountPhysicalLabel.setVisibility(View.GONE);
                                    tCpuCountLogicalLabel.setVisibility(View.GONE);
                                    tCpuFrequencyLabel.setVisibility(View.GONE);
                                    tCpuPercent = (TextView) findViewById(R.id.cpu_percent);
                                    tCpuMaxPercent = (TextView) findViewById(R.id.cpu_max_percent);
                                    tCpuCountPhysical = (TextView) findViewById(R.id.cpu_count_physical);
                                    tCpuCountLogical = (TextView) findViewById(R.id.cpu_count_logical);
                                    tCpuFrequency = (TextView) findViewById(R.id.cpu_frequency);
                                    tCpuPercent.setVisibility(View.GONE);
                                    tCpuMaxPercent.setVisibility(View.GONE);
                                    tCpuCountPhysical.setVisibility(View.GONE);
                                    tCpuCountLogical.setVisibility(View.GONE);
                                    tCpuFrequency.setVisibility(View.GONE);
                                    tMemoryStatsLabel = (TextView) findViewById(R.id.memory_stats_label);
                                    tMemoryTotalLabel = (TextView) findViewById(R.id.memory_total_label);
                                    tMemoryAvailableLabel = (TextView) findViewById(R.id.memory_available_label);
                                    tMemoryUsedLabel = (TextView) findViewById(R.id.memory_used_label);
                                    tMemoryPercentLabel = (TextView) findViewById(R.id.memory_percent_label);
                                    tMemoryStatsLabel.setVisibility(View.GONE);
                                    tMemoryTotalLabel.setVisibility(View.GONE);
                                    tMemoryAvailableLabel.setVisibility(View.GONE);
                                    tMemoryUsedLabel.setVisibility(View.GONE);
                                    tMemoryPercentLabel.setVisibility(View.GONE);
                                    tMemoryTotal = (TextView) findViewById(R.id.memory_total);
                                    tMemoryAvailable = (TextView) findViewById(R.id.memory_available);
                                    tMemoryUsed = (TextView) findViewById(R.id.memory_used);
                                    tMemoryPercent = (TextView) findViewById(R.id.memory_percent);
                                    tMemoryTotal.setVisibility(View.GONE);
                                    tMemoryAvailable.setVisibility(View.GONE);
                                    tMemoryUsed.setVisibility(View.GONE);
                                    tMemoryPercent.setVisibility(View.GONE);
                                }
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
     * Background Async Task to Load Computer Stats by making HTTP Request
     * */
    class LoadCpuStats extends AsyncTask<String, String, String> {

        /**
         * getting Computer Stats from url
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
                    // computer stats found
                    tracking_all_stats = Integer.parseInt(json.getString(TAG_TRACKING_ALL_STATS));
                    tracking_cpu = Integer.parseInt(json.getString(TAG_TRACKING_CPU));
                    tracking_memory = Integer.parseInt(json.getString(TAG_TRACKING_MEMORY));
                    tracking_disk = Integer.parseInt(json.getString(TAG_TRACKING_DISK));
                    if (tracking_all_stats == 1) {
                        systemBootTime = json.getString(TAG_SYSTEM_BOOT_TIME);
                        computerUser = json.getString(TAG_COMPUTER_USER);
                        if (tracking_cpu == 1) {
                            cpuPercent = Double.parseDouble(json.getString(TAG_CPU_PERCENT));
                            cpuMaxPercent = Double.parseDouble(json.getString(TAG_CPU_MAX_PERCENT));
                            cpuCountPhysical = Integer.parseInt(json.getString(TAG_CPU_COUNT_PHYSICAL));
                            cpuCountLogical = Integer.parseInt(json.getString(TAG_CPU_COUNT_LOGICAL));
                            cpuFrequency = Double.parseDouble(json.getString(TAG_CPU_FREQUENCY));
                        }
                        if (tracking_memory == 1) {
                            memoryTotal = Double.parseDouble(json.getString(TAG_MEMORY_TOTAL));
                            memoryAvailable = Double.parseDouble(json.getString(TAG_MEMORY_AVAILABLE));
                            memoryUsed = Double.parseDouble(json.getString(TAG_MEMORY_USED));
                            memoryPercent = Double.parseDouble(json.getString(TAG_MEMORY_PERCENT));
                        }
                        if (tracking_disk == 1) {

                        }
                    } else {
                        error = "Tracker not currently running";
                    }
                    //recievedCpuPercent = (int) Math.round(Double.parseDouble(json.getString(TAG_CPU_PERCENT)));
                    //recievedCpuMaxPercent = (int) Math.round(Double.parseDouble(json.getString(TAG_CPU_MAX_PERCENT)));
                }
            } catch (JSONException e) {
                e.printStackTrace();
            }
            return null;
        }
    }
}
