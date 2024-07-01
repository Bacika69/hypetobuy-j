q = "Nike Air Force 1 Low Tiffany &amp; Co. 1837"
if '&' in q:
    q = q.split('&')
    q = q[0]
    print(q)