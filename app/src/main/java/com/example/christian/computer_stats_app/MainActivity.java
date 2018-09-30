package com.example.christian.computer_stats_app;

import android.app.ProgressDialog;
import android.content.Intent;
import android.os.AsyncTask;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;

import org.apache.http.NameValuePair;
import org.apache.http.message.BasicNameValuePair;
import org.json.JSONException;
import org.json.JSONObject;

import java.net.URI;
import java.net.URISyntaxException;
import java.util.ArrayList;
import java.util.List;


public class MainActivity extends AppCompatActivity {

    private ProgressDialog pDialog;

    JSONParser jsonParser = new JSONParser();
    EditText inputComputerName;
    EditText inputPassword;

    private static URI url_login;

    static {
        try {
            url_login = new URI("http", "192.168.1.87:8888", "/computer_stats_connector/get_login_info.php", null, null);
        } catch (URISyntaxException e) {
            e.printStackTrace();
        }
    }

    private static final String TAG_SUCCESS = "success";
    private static final String TAG_CID = "cid";

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        // Edit Text
        inputComputerName = (EditText) findViewById(R.id.inputComputerName);
        inputPassword = (EditText) findViewById(R.id.inputPassword);

        // Create button
        Button btnLogin = (Button) findViewById(R.id.btnLogin);

        // Button click event
        btnLogin.setOnClickListener(new View.OnClickListener() {

            @Override
            public void onClick(View view) {
                // Login in background thread
                new Login().execute();
            }
        });
    }

    class Login extends AsyncTask<String, String, String> {

        /**
         * Before starting background thread Show Progress Dialog
         * */
        @Override
        protected void onPreExecute() {
            super.onPreExecute();
            pDialog = new ProgressDialog(MainActivity.this);
            pDialog.setMessage("Logging In..");
            pDialog.setIndeterminate(false);
            pDialog.setCancelable(true);
            pDialog.show();
        }

        /**
         * Logging in
         * */
        protected String doInBackground(String... args) {
            String computerName = inputComputerName.getText().toString();
            String password = inputPassword.getText().toString();

            // Building Parameters
            List<NameValuePair> params = new ArrayList<NameValuePair>();
            params.add(new BasicNameValuePair("computer_name", computerName));
            params.add(new BasicNameValuePair("password", password));

            // getting JSON Object
            // Note that create product url accepts POST method
            JSONObject json = jsonParser.makeHttpRequest(url_login,
                    "POST", params);

            // check log cat from response
            Log.d("Create Response", json.toString());

            // check for success tag
            try {
                int success = json.getInt(TAG_SUCCESS);

                if (success == 1) {
                    // successfully created product
                    Intent i = new Intent(getApplicationContext(), ViewStats.class);
                    i.putExtra("cid", json.getString(TAG_CID));
                    startActivity(i);

                    // closing this screen
                    finish();
                } else {
                    // failed to create product
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
            // dismiss the dialog once done
            pDialog.dismiss();
        }

    }
}
