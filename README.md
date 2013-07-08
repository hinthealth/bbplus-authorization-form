bbplus-authorization-form
=========================

This project demonstrates a sample patient authorization form a provider
may use to allow patients to configure their enrollment for BlueButton+ data
transfer.

A demo of this application is deployed at:
  https://bb-authorization-form-dot-healthio-dev.appspot.com/

It supports the following features:
- Addition of multiple Direct addresses per patients.
- Email notifications upon changing frequency settings.
- Simple Direct address validation.

This patient authorization form is intended to demonstrate a clean user
experience that BlueButton+ providers can use. It is implemented in simple,
easy-to-understand Python and JavaScript, which means it can be integrated
easily into an existing system.

This sample runs on Google App Engine, which allows providers to spin up
their own patient management instance easily. An abstract data storage
class is implemented, making it easily portable off of App Engine onto
another platorm.

To run a development server:

1. Download the [Google App Engine SDK for Python](https://developers.google.com/appengine/downloads)
2. Run `./utils/run.sh`

To deploy to App Engine:

1. Create an application (or use an existing one) at http://appengine.google.com
2. Run `./utils/deploy.sh --application=<app id>`
