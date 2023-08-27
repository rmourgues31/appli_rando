FROM eclipse-temurin:20.0.2_9-jre-alpine

WORKDIR /otp
COPY . /otp

EXPOSE 8080
CMD ["java", "-Xmx2G", "-jar", "otp-2.3.0-shaded.jar", "--load", "."]