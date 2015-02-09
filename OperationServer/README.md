
PHP server has to tell  the operation server class id by post.

    postdata={"class_id":1}

    post("http://127.0.0.1:8888/createstream", data=postdata)

Client get the stream by post.

    getdata={"calss_id":1}

    post("http://127.0.0.1:8888/getstream", data=getdata)

