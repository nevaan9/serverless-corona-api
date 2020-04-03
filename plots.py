# serverless invoke local --function functionName
from bokeh.embed import json_item
from bokeh.plotting import figure
import json


def main(event, context):
    try:
        x = [1, 2, 3, 4, 5]
        y = [6, 7, 8, 9, 10]

        plot = figure()

        plot.line(x, y, line_width=3)

        plot.circle(x, y, fill_color='white', size=10)

        plot_json = json.dumps(json_item(plot, 'myplot'))
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Credentials': True,
            },
            'body': plot_json,
        }
    except Exception as exc:
        print(exc)
        return {
            'statusCode': 400,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Credentials': True,
            },
            'body': '{"status": "fail"}',
        }

if __name__ == "__main__":
    main('', '')

