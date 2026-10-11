package com.megasuite.cleanicon;

import android.app.Activity;
import android.os.Bundle;
import android.view.Gravity;
import android.widget.ScrollView;
import android.widget.TextView;

/**
 * 极简说明页：让图标包 App 能被启动，并告诉用户如何应用。
 * 图标包本身不需要任何业务逻辑。
 */
public class MainActivity extends Activity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        float density = getResources().getDisplayMetrics().density;
        int pad = (int) (24 * density);

        TextView tv = new TextView(this);
        tv.setText(R.string.usage);
        tv.setTextSize(16);
        tv.setLineSpacing(0, 1.3f);
        tv.setGravity(Gravity.START);
        tv.setPadding(pad, pad, pad, pad);

        ScrollView scroll = new ScrollView(this);
        scroll.addView(tv);
        setContentView(scroll);
    }
}
