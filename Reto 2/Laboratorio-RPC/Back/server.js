var express = require('express')
var app = express()


app.get('/listfiles', function(req, res) {
  res.send('Hello World!')
});
app.get('/findfiles/:id', (req,res)=>{
  const userId = req.parms.id;
  res.send(`recibido el parametro id: ${userId}`)
});

app.listen(port, () => {
  console.log(`Example app listening on port ${port}`)
})
