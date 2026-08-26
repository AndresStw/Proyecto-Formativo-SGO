const handleRegister = async (e) => {
  e.preventDefault();
  
  const response = await fetch('http://localhost:3000/register', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      email: 'cliente@saborcaleno.com',
      password: '123456'
    })
  });
  
  const data = await response.json();
  
  if (response.ok) {
    // Guardar el token
    localStorage.setItem('token', data.accessToken);
    console.log('Usuario registrado:', data.user);
  } else {
    console.error('Error:', data);
  }
};