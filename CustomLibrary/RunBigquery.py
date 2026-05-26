from google.cloud import bigquery

def run_bigquery(query):
    client = bigquery.Client()
    query_job = client.query(query)
    results = query_job.result()
    rows = []
    #Iterate over the RowIterator object
    for row in results:
        rows.append(row)
    return rows

