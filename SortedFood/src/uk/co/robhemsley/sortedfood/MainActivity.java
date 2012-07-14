package uk.co.robhemsley.sortedfood;

import org.json.JSONArray;
import org.json.JSONException;


import android.os.Bundle;
import android.app.Activity;
import android.util.Log;
import android.view.Menu;
import android.view.MenuItem;
import com.biggu.barcodescanner.client.android.Intents;
import com.google.gson.Gson;
import com.loopj.android.http.AsyncHttpClient;
import com.loopj.android.http.AsyncHttpResponseHandler;
import com.loopj.android.http.RequestParams;

import android.app.Activity;
import android.content.Intent;
import android.os.Bundle;
import android.view.View;
import android.view.View.OnClickListener;
import android.widget.Button;
import android.widget.TextView;
import android.widget.Toast;

public class MainActivity extends Activity {
	
	private static final int SCANNER_REQUEST_CODE = 0;

	@Override
	public void onCreate(Bundle savedInstanceState) {
		super.onCreate(savedInstanceState);
		setContentView(R.layout.main);

		Button button = (Button)findViewById(R.id.btn);
		
		button.setOnClickListener(new OnClickListener() {
			public void onClick(View v) {

				Intent intent = new Intent(v.getContext(), ScannerActivity.class);
				intent.putExtra(Intents.Preferences.ENABLE_BEEP, true);
				intent.putExtra(Intents.Preferences.ENABLE_VIBRATE, true);

				((Activity)v.getContext()).startActivityForResult(intent, SCANNER_REQUEST_CODE);
			}
		});
	}

	@Override
	public void onActivityResult(int requestCode, int resultCode, Intent data) {
		
		if (resultCode == Activity.RESULT_OK && requestCode == SCANNER_REQUEST_CODE) {

			Bundle extras = data.getExtras();
			String result = extras.getString("SCAN_RESULT");
			TextView textView = (TextView)findViewById(R.id.txt);
			textView.setText(result);
			
			RequestParams params = new RequestParams();
			params.put("key", "value");
			params.put("more", "data");
			
			AsyncHttpClient client = new AsyncHttpClient();
			String url = "http://sorted.robhemsley.webfactional.com/API/v0/Product/UK/" + result.toString() + "/";
			Log.e("", url);
			client.get(url, new AsyncHttpResponseHandler() {
			    @Override
			    public void onSuccess(String response) {
			    	Log.e("", response);
			    
			    	 // Now do the magic.
			    	JsonProduct data = new Gson().fromJson(response.toString(), JsonProduct.class);

			        // Show it.
			        Log.e("CAT", data.toString());
			
			    }
			});
			
			Toast.makeText(getApplicationContext(), result, Toast.LENGTH_LONG).show();
		}
	}}