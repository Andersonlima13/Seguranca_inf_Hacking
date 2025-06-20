const express = require('express');
const app = express();
app.use(express.json());

app.post('https://api.pushio.com/webpushlistener/wpl/v3/signal/test123/test456', (req, res) => {
  console.log(`Recebido: ${req.params.account} | ${req.params.key}`);
  res.json({status: "success", data: req.body});
});

app.listen(3000, () => console.log('Mock API rodando'));