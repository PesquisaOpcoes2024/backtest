// const express = require('express');
// const axios = require('axios');

// const app = express();
// const PORT = 3000;

// app.get('/data', async (req, res) => {
//     try {
//         const response = await axios.get('http://localhost:5000/api/data');
//         res.json(response.data);
//     } catch (error) {
//         console.error('Erro ao conectar com o backend Python:', error.message);
//         res.status(500).json({ error: 'Erro ao conectar com o backend Python' });
//     }
// });

// app.listen(PORT, () => {
//     console.log(`Servidor frontend rodando na porta ${PORT}`);
// });

const express = require('express');
const axios = require('axios');
const path = require('path');

const app = express();
const PORT = 5000;

// Middleware para servir o build do React
app.use(express.static(path.join(__dirname, 'Front', 'build')));

// Endpoint para dados do backend Python
app.get('/data', async (req, res) => {
    try {
        const response = await axios.get('http://localhost:5000/api/data');  // Backend Python
        res.json(response.data);
    } catch (error) {
        console.error('Erro ao conectar com o backend Python:', error.message);
        res.status(500).json({ error: 'Erro ao conectar com o backend Python' });
    }
});

// Para qualquer outra rota, servir o frontend React
app.get('*', (req, res) => {
    res.sendFile(path.join(__dirname, 'Front', 'build', 'index.html'));
});

app.listen(PORT, () => {
    console.log(`Servidor rodando na porta ${PORT}`);
});
