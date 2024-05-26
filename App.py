from flask import Flask, request, render_template, redirect, url_for, flash
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from sklearn.impute import SimpleImputer
import os

app = Flask(__name__)
app.secret_key = "supersecretkey"

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

scatterplot_data = None


@app.route("/", methods=["GET", "POST"])
def index():
    global scatterplot_data
    if request.method == "POST":
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(filepath)
            scatterplot_data = process_data_file(filepath, file.filename)
            scatterplot_data = clean_data(scatterplot_data)
            return redirect(url_for('explore'))

    return render_template("index.html")


@app.route('/explore', methods=['GET', 'POST'])
def explore():
    scatterplot_json = []
    heatmap_figs = []
    bar_chart_figs = []
    pair_plot_json = []
    histogram_figs = []
    scatterplot_3d_json = []
    time_series_json = []
    box_plot_json = []
    linear_regression_json = []

    global scatterplot_data
    if scatterplot_data is None:
        return redirect(url_for('index'))

    scatterplot_fig = generate_scatterplot(scatterplot_data)
    scatterplot_json = scatterplot_fig.to_json()

    heatmap_figs = []
    bar_chart_figs = []
    for column in scatterplot_data.columns:
        if pd.api.types.is_numeric_dtype(scatterplot_data[column]):
            heatmap_fig = generate_heatmap(scatterplot_data, column)
            heatmap_json = heatmap_fig.to_json()
            heatmap_figs.append((column, heatmap_json))
        else:
            bar_chart_fig = generate_bar_chart(scatterplot_data, column)
            bar_chart_json = bar_chart_fig.to_json()
            bar_chart_figs.append((column, bar_chart_json))

            pair_plot_fig = generate_pair_plot(scatterplot_data)
            pair_plot_json = pair_plot_fig.to_json()

    histogram_figs = []
    for column in scatterplot_data.columns:
        histogram_fig = px.histogram(scatterplot_data,
                                     x=column,
                                     title=f"Histogram of {column}")
        histogram_json = histogram_fig.to_json()
        histogram_figs.append((column, histogram_json))

    scatterplot_3d_fig = px.scatter_3d(
        scatterplot_data,
        x=scatterplot_data.columns[0],
        y=scatterplot_data.columns[1],
        z=scatterplot_data.columns[2],
    )
    scatterplot_3d_json = scatterplot_3d_fig.to_json()

    time_series_fig = generate_time_series_plot(scatterplot_data)
    time_series_json = time_series_fig.to_json()

    box_plot_fig = generate_box_plot(scatterplot_data,
                                     scatterplot_data.columns[2])
    box_plot_json = box_plot_fig.to_json()

    selected_columns = [
        scatterplot_data.columns[0],
        scatterplot_data.columns[1],
    ]
    linear_regression_fig = generate_linear_regression_plot(scatterplot_data)

    linear_regression_json = linear_regression_fig.to_json()

    return render_template("explore.html",
                           scatterplot_json=scatterplot_json,
                           heatmap_figs=heatmap_figs,
                           bar_chart_figs=bar_chart_figs,
                           pair_plot_json=pair_plot_json,
                           histogram_figs=histogram_figs,
                           scatterplot_3d_json=scatterplot_3d_json,
                           time_series_json=time_series_json,
                           box_plot_json=box_plot_json,
                           linear_regression_json=linear_regression_json)


def allowed_file(filename):
    return '.' in filename and filename.rsplit(
        '.', 1)[1].lower() in {'csv', 'xlsx'}


def process_data_file(filepath, filename):
    if filename.endswith(".xlsx"):
        df = pd.read_excel(filepath)
    elif filename.endswith(".csv"):
        df = pd.read_csv(filepath)
    else:
        raise ValueError(
            "Unsupported file type. Please upload a CSV or Excel file.")
    return df


def clean_data(data):
    imputer = SimpleImputer(strategy="mean")
    cleaned_data = pd.DataFrame()
    for col in data.columns:
        if pd.api.types.is_numeric_dtype(data[col]):
            cleaned_data[col] = imputer.fit_transform(data[col].values.reshape(
                -1, 1)).flatten()
        elif pd.api.types.is_datetime64_any_dtype(data[col]):
            cleaned_data[col] = pd.to_numeric(data[col])
        else:
            raise ValueError(f"Unsupported data type in column '{col}'")
    return cleaned_data


def generate_pair_plot(data):
    fig = go.Figure(data=go.Splom(dimensions=[
        dict(label=column, values=data[column]) for column in data.columns
    ]))
    return fig


def clean_data(data):
    imputer = SimpleImputer(strategy="mean")
    cleaned_data = pd.DataFrame()
    for col in data.columns:
        if pd.api.types.is_numeric_dtype(data[col]):
            cleaned_data[col] = imputer.fit_transform(data[col].values.reshape(
                -1, 1)).flatten()
        elif pd.api.types.is_datetime64_any_dtype(data[col]):
            cleaned_data[col] = pd.to_numeric(data[col])
        else:
            print(
                f"Skipping column '{col}' because it is not numeric or datetime."
            )
    return cleaned_data


def generate_pair_plot(data):
    fig = go.Figure(data=go.Splom(dimensions=[
        dict(label=column, values=data[column]) for column in data.columns
    ]))
    return fig


def generate_scatterplot(data, color_column=None, size_column=None):
    if size_column is not None:
        # Replace negative size values with zero or their absolute value
        data[size_column] = data[size_column].apply(lambda x: max(x, 0))

    fig = px.scatter(
        data,
        x=data.columns[0],
        y=data.columns[1],
        color=color_column,
        size=size_column,
        labels={
            data.columns[0]: "X-axis",
            data.columns[1]: "Y-axis"
        },
    )

    return fig


def generate_heatmap(data, column):
    numeric_columns = data.columns[data.dtypes.apply(
        lambda c: pd.api.types.is_numeric_dtype(c))]
    correlation_matrix = data[numeric_columns].corr()
    fig = px.imshow(
        correlation_matrix,
        labels=dict(color="Correlation"),
        color_continuous_scale="Viridis",
    )
    return fig


def generate_bar_chart(data, column):
    counts = data[column].value_counts()
    bar_chart_fig = px.bar(
        x=counts.index,
        y=counts.values,
        labels={
            column: "Count",
            "index": column
        },
        title=f"Counts of {column}",
    )
    return bar_chart_fig


def generate_time_series_plot(data):
    time_series_fig = px.line(
        data,
        x=data.columns[0],
        y=data.columns[1],
        labels={
            data.columns[0]: "Time",
            data.columns[1]: "Value"
        },
    )
    return time_series_fig


def generate_box_plot(data, color_column):
    box_plot_fig = px.box(
        data,
        x=color_column,
        y=data.columns[1],
        color=color_column,
        labels={data.columns[1]: "Numerical Value"},
    )
    return box_plot_fig


def generate_linear_regression_plot(data):
    selected_columns = [data.columns[0], data.columns[1]]
    if data[selected_columns].isnull().any().any():
        imputer = SimpleImputer(strategy="mean")
        for col in selected_columns:
            if pd.api.types.is_datetime64_any_dtype(data[col]):
                data[col] = pd.to_numeric(data[col])
            elif pd.api.types.is_numeric_dtype(data[col]):
                data[col] = imputer.fit_transform(data[col].values.reshape(
                    -1, 1)).flatten()
            else:
                raise ValueError(f"Unsupported data type in column '{col}'")

    X = data[selected_columns[0]].values.reshape(-1, 1)
    y = data[selected_columns[1]].values.reshape(-1, 1)

    X_train, X_test, y_train, y_test = train_test_split(X,
                                                        y,
                                                        test_size=0.2,
                                                        random_state=42)

    model = LinearRegression()
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)

    mse = mean_squared_error(y_test, y_pred)

    scatter_fig = generate_scatterplot(data, selected_columns[0],
                                       selected_columns[1])

    regression_line = go.Scatter(x=X_test.flatten(),
                                 y=y_pred.flatten(),
                                 mode="lines",
                                 name="Regression Line")

    linear_regression_fig = go.Figure(
        data=[scatter_fig.data[0], regression_line])

    linear_regression_fig.update_layout(
        title=f"Linear Regression (MSE: {mse:.2f})",
        xaxis_title=selected_columns[0],
        yaxis_title=selected_columns[1],
    )

    return linear_regression_fig


if __name__ == "__main__":
    app.run(debug=True)
