# Introduction

The Rebilly API is built on HTTP.  Our API is RESTful.  It has predictable resource URLs.  It returns HTTP response codes to indicate errors.  It also accepts and returns JSON in the HTTP body.  You can use your favorite HTTP/REST library for your programming language to use Rebilly's API, or you can use one of our SDKs (currently available in [PHP](https://github.com/Rebilly/rebilly-php) and [C#](https://github.com/Rebilly/rebilly-dotnet-client)).

More examples: https://www.commbox.io/api/#operation/Send_Templated_Message

# Authentication

When you sign up for an account, you are given your first API key. You can generate additional API keys, and delete API keys (as you may need to rotate your keys in the future). You authenticate to the Rebilly API by providing your secret key in the request header.


Rebilly offers three forms of authentication:  private key, JSON Web Tokens, and public key.
- private key: authenticates each request by searching for the presence of an HTTP header: REB-APIKEY.
- JWT: authenticates each request by the HTTP header: Authorization.
- public key: authenticates by the HTTP header: REB-AUTH (read more on this below). 

Rebilly also offers JSON Web Tokens (JWT) authentication, where you can control the specific granular permissions and expiration for that JWT.  We call our resource for generating JWT [Sessions](#tag/Sessions).

Rebilly also has a client-side authentication scheme that uses an apiUser and HMAC-SHA1 signature (only for the Tokens resource), so that you may safely create tokens from the client-side without compromising your secret keys.

Never share your secret keys. Keep them guarded and secure. The client-side authentication scheme uses one HTTP header named REB-AUTH.
#  Python SDK

For all Python SDK examples provided in this spec you will need to configure `client`.

You may do it like this:

```python
$client = new Rebilly\\Client([     'apiKey' => 'YourApiKeyHere',     'baseUrl' => 'https://api.rebilly.com', ]);
```

# API Informatons

## Meta informations
| Resource  | Description                             | Value |
|-----------|-----------------------------------------|-------|
| `Memory`  | Memory Maximum memory size, in GB 4     | 4     |
| `Request` | Maximum time before timeout, in seconds | 45-90 |

## Rate Limits
    The following rate limits apply to the Cloud Run Admin API. They do not apply to the requests reaching your deployed Cloud Run (fully managed) services.

| Quota                              | Description                                                                                                                                                     | Limit                 |
| ------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------|-----------------------|
| Cloud Run Admin API read requests  | The number of API reads per 100 seconds per project. This is not the number of read requests to your Cloud Run (fully managed) services, which is not limited.  | 1,000 per 100 seconds |
| Cloud Run Admin API write requests | The number of API writes per 100 seconds per project. This is not the number of write requests to your Cloud Run (fully managed) services, which is not limited | 100 per 100 seconds   |

# Architecture
![Cloud Run](https://miro.medium.com/max/2664/1*SFaD-r603Zp8Vhrq39lQjA.png)
The Architecture describes the request:
1. first the request will be created
2. then the request will be preprocessed
3. the **price** will be added
4. _tax_ can be kursiv
5. and then we load the `model`
