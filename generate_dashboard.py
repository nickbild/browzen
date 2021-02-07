import sqlite3


# Create SQLite3 DB connection.
def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)

    return conn


def print_header(dashboard):
    dashboard.write("""
    <!DOCTYPE html>
    <html>
      <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>BrowZen Dashboard</title>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/2.9.4/Chart.min.js"></script>
      </head>
      <body bgcolor="#e0e0d1">

        <div style="width: 1050px; display: block; margin-left: auto; margin-right: auto;">

        <div>
    	     <canvas id="myChart1" style="width:500px; float: left;"></canvas>
        </div>

        <div>
    	     <canvas id="myChart2" style="width:500px; float: left;"></canvas>
        </div>

        <div>
    	     <canvas id="myChart3" style="width:500px; float: left;"></canvas>
        </div>

        <div>
    	     <canvas id="myChart4" style="width:500px; float: left;"></canvas>
        </div>

        <div>
    	     <canvas id="myChart5" style="width:500px; float: left;"></canvas>
        </div>

        <div>
    	     <canvas id="myChart6" style="width:500px; float: left;"></canvas>
        </div>

        </div>

        <script>
    """)

    return None


def print_footer(dashboard):
    dashboard.write("""
        </script>

      </body>
    </html>
    """)

    return None


def print_chart(dashboard, domain, chart_num):
    emotions_conn = create_connection("emotional_states.db")

    # Get all emotion data for this domain.
    sql = "select * from url_emotions where url = '{0}'".format(domain)
    cursor = emotions_conn.cursor()
    cursor.execute(sql)
    records = cursor.fetchall()

    # Get counts for each emotion.
    angry = disgust = fear = happy = sad = surprise = neutral = 0
    for record in records:
        if record[1] == 0:
            angry = record[2]
        elif record[1] == 1:
            disgust = record[2]
        elif record[1] == 2:
            fear = record[2]
        elif record[1] == 3:
            happy = record[2]
        elif record[1] == 4:
            sad = record[2]
        elif record[1] == 5:
            surprise = record[2]
        elif record[1] == 6:
            neutral = record[2]

    dashboard.write("""
      var ctx = document.getElementById('myChart{1}').getContext('2d');
      var myChart{1} = new Chart(ctx, {{
          type: 'doughnut',
          data: {{
            labels: ["Angry","Disgust", "Fear", "Happy", "Sad", "Surprise", "Neutral"],
            datasets: [{{
                data: [{2},{3},{4},{5},{6},{7},{8}],
                borderColor:[
                  "#fc0202",
                  "#e2d303",
                  "#ff6600",
                  "#00e617",
                  "#004bd8",
                  "#f402e0",
                  "#ffffff",

                ],
                backgroundColor: [
                  "rgb(252,2,2,0.5)",
                  "rgb(252,237,22,0.5)",
                  "rgb(255,102,0,0.5)",
                  "rgb(91,255,108,0.5)",
                  "rgb(0,75,216,0.5)",
                  "rgb(244,2,224,0.5)",
                  "rgb(255,255,255,0.5)",

                ],
                borderWidth:2,
              }}]
          }},
        options: {{
          title: {{
              display: true,
              text: '{0}'
          }},
          legend: {{
            display: false
         }},
          responsive: false,
          scales: {{
            xAxes: [{{
               display: false,
            }}],
            yAxes: [{{
               display: false,
            }}],
          }}
        }},

      }});
    """.format(domain, str(chart_num), str(angry), str(disgust), str(fear), str(happy), str(sad), str(surprise), str(neutral)))

    return None


def main():
    dashboard = open("dashboard.html", "w")

    print_header(dashboard)

    domains = ('hackster.io', 'hackaday.com', 'twitter.com', 'facebook.com', 'reddit.com', 'google.com')
    chart_num = 1
    for domain in domains:
        print_chart(dashboard, domain, chart_num)
        chart_num += 1

    print_footer(dashboard)

    return None


if __name__ == "__main__":
    main()
