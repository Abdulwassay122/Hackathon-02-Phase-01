// Script to verify API endpoints
// Usage: node verify-api-endpoints.js

const API_BASE_URL = process.env.API_BASE_URL || 'http://localhost:8000';

async function verifyEndpoint(method, endpoint, expectedStatus = 200) {
  try {
    const response = await fetch(`${API_BASE_URL}${endpoint}`, {
      method,
      headers: {
        'Content-Type': 'application/json',
      },
    });

    console.log(`${method} ${endpoint}: ${response.status} ${response.status === expectedStatus ? '✓' : '✗'}`);
    return response.status === expectedStatus;
  } catch (error) {
    console.log(`${method} ${endpoint}: Error - ${error.message} ✗`);
    return false;
  }
}

async function verifyEndpoints() {
  console.log('Verifying API endpoints...\n');

  // Verify health endpoint
  await verifyEndpoint('GET', '/health', 200);

  // Verify API endpoints exist (will return 401 without auth, but should not return 404)
  const endpointsToCheck = [
    ['GET', '/api/tasks'],
    ['POST', '/api/tasks'],
    ['PUT', '/api/tasks/1'],
    ['DELETE', '/api/tasks/1'],
    ['PATCH', '/api/tasks/1/complete'],
    ['POST', '/auth/login'],
    ['POST', '/auth/logout'],
    ['GET', '/auth/me']
  ];

  for (const [method, endpoint] of endpointsToCheck) {
    try {
      const response = await fetch(`${API_BASE_URL}${endpoint}`, {
        method,
        headers: {
          'Content-Type': 'application/json',
        },
      });

      // For endpoints that require auth, we expect 401, not 404
      const isValid = response.status !== 404;
      console.log(`${method} ${endpoint}: ${response.status} ${isValid ? '✓' : '✗'}`);
    } catch (error) {
      console.log(`${method} ${endpoint}: Error - ${error.message} ✗`);
    }
  }

  console.log('\nVerification complete!');
}

verifyEndpoints().catch(console.error);