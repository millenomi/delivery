# Ad Hoc OTA for App Engine

This is a Google App Engine application that handles over-the-air iOS app distribution (for iOS 4.0+). It's a work-in-progress, not yet finished.

## Working API

### `/com.apple.ios/provisioning/add`

* `GET` to have a simple upload form for a provisioning profile.

* `POST` (`multipart/form-data`) to upload a provisioning profile. Arguments:

 * `profile`: The contents of the provisioning profile.

### `/com.apple.ios/provisioning/<UUID>`

* `GET` to download the uploaded provisioning profile with the given UUID.
