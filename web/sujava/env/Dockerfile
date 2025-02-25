FROM ubuntu:20.04

RUN mkdir /app
RUN mkdir /app/Java8
RUN mkdir /app/Java_8
RUN mkdir /ctf

ENV FLAG=SUCTF{Y0u_Re41ly_a_JdbC_M4st3r_And_H4v3_A_G0od_d4y!!!}
WORKDIR /app
COPY suctf_fl4g /ctf
COPY suJava-0.0.1-SNAPSHOT.jar /app/
COPY Java8 /app/Java8
#COPY Java_8 /app/Java_8
COPY start.sh /
RUN chmod +x /start.sh

CMD ["/start.sh"]
