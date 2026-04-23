const express = require('express');
const axios = require('axios');
const app = express();

app.set('view engine', 'ejs');
app.use(express.urlencoded({ extended: true }));
app.use(express.json());

const FLASK_BACKEND = process.env.FLASK_BACKEND || 'http://backend:5000';

// Serve the form
app.get('/', (req, res) => {
    res.render('index', { error: null, success: null });
});

// Handle form submission
app.post('/submit', async (req, res) => {
    const { name, email, message } = req.body;

    try {
        const response = await axios.post(`${FLASK_BACKEND}/submit`, {
            name,
            email,
            message
        });

        res.render('index', { 
            success: response.data.message, 
            error: null 
        });

    } catch (err) {
        const error = err.response?.data?.error || 'Something went wrong';
        res.render('index', { 
            error: error, 
            success: null 
        });
    }
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, '0.0.0.0', () => {
    console.log(`Frontend running on port ${PORT}`);
});
