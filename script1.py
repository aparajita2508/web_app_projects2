from flask import Flask, render_template

app=Flask(__name__)

@app.route('/plot/')
def plot():
    from pandas_datareader import data
    import datetime
    from bokeh.plotting import figure, show, output_file
    from bokeh.io import output_notebook
    from bokeh.embed import components
    from bokeh.resources import CDN

    start = datetime.datetime(2017, 7, 1)
    end = datetime.datetime(2017, 7, 25)
    df = data.DataReader(name="GOOG", data_source="google", start=start, end=end)
    output_notebook()

    def inc_dec(c, o):
        if c > o:
            value = "Increase"

        elif c < o:
            value = "Decrease"
        return value

    df["Status"] = [inc_dec(c, o) for c, o in zip(df.Close, df.Open)]

    df["Middle"] = (df.Open + df.Close) / 2
    df["Height"] = abs(df.Open - df.Close)

    p = figure(x_axis_type='datetime', width=1000, height=300, responsive=True)
    p.title.text = 'Candlestick Chart'
    p.grid.grid_line_alpha = 0.3
    hours_12 = 12 * 60 * 60 * 1000
    p.segment(df.index, df.High, df.index, df.Low)
    p.rect(df.index[df.Status == "Increase"], df.Middle[df.Status == "Increase"],
           hours_12, df.Height[df.Status == "Increase"],
           fill_color="#808080", line_color="black")
    p.rect(df.index[df.Status == "Decrease"], df.Middle[df.Status == "Decrease"],
           hours_12, df.Height[df.Status == "Decrease"],
           fill_color="#FF69B4", line_color="black")
    script1, div1, = components(p)
    cdn_js = CDN.js_files[0]
    cdn_css = CDN.css_files[0]
    return render_template("plot.html", script1 = script1, div1 = div1, cdn_css = cdn_css,cdn_js = cdn_js)

@app.route('/')
def home():
    return render_template("home.html")

@app.route('/about/')
def about():
    return render_template("about.html")

if __name__=="__main__":
    app.run(debug=True, port=1234)
