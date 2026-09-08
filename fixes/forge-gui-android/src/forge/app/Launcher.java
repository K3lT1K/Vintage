package forge.app;

import android.app.Activity;
import android.content.Intent;
import android.net.Uri;
import android.os.Bundle;
import android.os.Handler;
import android.os.Looper;
import forge.gui.GuiBase;

import java.io.BufferedReader;
import java.io.InputStream;
import java.io.InputStreamReader;

public class Launcher extends Activity {
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        android.widget.TextView status = new android.widget.TextView(this);
        status.setText("Vintage Solo\nPreparing offline resources…");
        status.setTextColor(android.graphics.Color.WHITE);
        status.setBackgroundColor(android.graphics.Color.rgb(20, 30, 28));
        status.setTextSize(22);
        status.setGravity(android.view.Gravity.CENTER);
        setContentView(status);

        // Main extends AndroidApplication: its LibGDX fields must be ready before
        // Android calls onResume. Extract in this plain Activity instead.
        new Thread(() -> {
            try {
                String version;
                try (BufferedReader reader = new BufferedReader(new InputStreamReader(
                        getAssets().open("vintage-res.version"), java.nio.charset.StandardCharsets.UTF_8))) {
                    version = reader.readLine();
                }
                forge.util.VintageResources.install(getAssets().open("vintage-res.zip"),
                        new java.io.File(getFilesDir(), "VintageSolo"), version);
                runOnUiThread(() -> {
                    if (isFinishing() || isDestroyed()) { return; }
                    Intent main = new Intent(Launcher.this, Main.class);
                    main.setFlags(Intent.FLAG_ACTIVITY_REORDER_TO_FRONT);
                    startActivity(main);
                    Intent intent = getIntent();
                    sendIntent(intent, intent.getAction(), intent.getType());
                    finish();
                    overridePendingTransition(android.R.anim.fade_in, android.R.anim.fade_out);
                });
            } catch (Exception error) {
                android.util.Log.e("VintageStartup", "Resource installation failed", error);
                runOnUiThread(() -> {
                    if (isFinishing() || isDestroyed()) { return; }
                    new android.app.AlertDialog.Builder(this)
                            .setTitle("Vintage Solo: resources")
                            .setMessage("Cannot install bundled resources: " + error)
                            .setPositiveButton("Close", (dialog, which) -> finish()).show();
                });
            }
        }, "Vintage resource install").start();
    }

    private void sendIntent(Intent intent, String action, String type) {
        if (Intent.ACTION_SEND.equals(action) && type != null) {
            final Handler handler = new Handler();
            handler.postDelayed(() -> {
                if ("text/plain".equals(type)) {
                    Uri textUri = intent.getParcelableExtra(Intent.EXTRA_STREAM);
                    if (textUri != null) {
                        try {
                            InputStream in = getContentResolver().openInputStream(textUri);
                            BufferedReader r = new BufferedReader(new InputStreamReader(in));
                            StringBuilder total = new StringBuilder();
                            for (String line; (line = r.readLine()) != null; ) {
                                total.append(line).append('\n');
                            }
                            GuiBase.getInterface().copyToClipboard(total.toString());
                        } catch (Exception e) {
                            e.printStackTrace();
                        }
                    } else {
                        try {
                            GuiBase.getInterface().copyToClipboard(intent.getStringExtra(Intent.EXTRA_TEXT));
                        } catch (Exception e) {
                            e.printStackTrace();
                        }
                    }
                }
            }, 1500);
        }
    }
    @Override
    protected void onNewIntent(Intent intent) {
        super.onNewIntent(intent);
        setIntent(intent);
        String action = intent.getAction();
        String type = intent.getType();

        if (Intent.ACTION_SEND.equals(action) && type != null) {
            new Handler(Looper.getMainLooper()).postDelayed(() -> {
                if ("text/plain".equals(type)) {
                    Uri textUri = intent.getParcelableExtra(Intent.EXTRA_STREAM);
                    if (textUri != null) {
                        try {
                            InputStream in = getContentResolver().openInputStream(textUri);
                            BufferedReader r = new BufferedReader(new InputStreamReader(in));
                            StringBuilder total = new StringBuilder();
                            for (String line; (line = r.readLine()) != null; ) {
                                total.append(line).append('\n');
                            }
                            GuiBase.getInterface().copyToClipboard(total.toString());
                        } catch (Exception e) {
                            e.printStackTrace();
                        }
                    } else {
                        try {
                            GuiBase.getInterface().copyToClipboard(intent.getStringExtra(Intent.EXTRA_TEXT));
                        } catch (Exception e) {
                            e.printStackTrace();
                        }
                    }
                }
            }, 1500);
        }
    }
}
