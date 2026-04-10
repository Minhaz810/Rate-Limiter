# Where to Put the Rate Limiter

## Placement Options

| Location | Description |
|----------|-------------|
| **Client-Side** | Implemented on the client side — unreliable. |
| **Server-Side** | Implemented on the server side. |
| **Middleware** | Implemented between client and server. |
| **API Gateway** | Implemented on the API Gateway. Typically seen in cloud microservices. |

---

## Guidelines for Implementing a Rate Limiter

1. Make sure your current technology stack (e.g. programming language, cache service) is efficient to implement rate limiting.
2. Identify the rate limiting algorithm that fits your business needs.
3. Implement on the server side if you need full control.
4. If you already have microservices and an API Gateway, then implement rate limiting on the API Gateway.
5. If you don't have enough resources to build a rate limiter, then use a third-party rate limiting service.

---

## Algorithms for Rate Limiting

- **Token Bucket**
- **Leaking Bucket**
- **Fixed Window Counter**
- **Sliding Window Log**
- **Sliding Window Counter**
