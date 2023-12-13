// escritura.js
const express = require('express');
const mysql = require('mysql');
const bodyParser = require('body-parser');
const amqp = require('amqplib');
const mongoose = require('mongoose');
// Configuración de RabbitMQ
const rabbitMqURL = 'amqp://localhost';
const exchangeName = 'escritura_exchange'; // Usar el exchange principal
const queueName = 'escritura_queue'; // Usar la cola principal
const routingKey = 'escritura'; // Usar la routing key principal


const app = express();
app.use(bodyParser.json());

const PUERTO = 3000;

const conexion = mysql.createConnection({
    host: 'db4free.net',
    database: 'bd_brandon',
    user: 'herrera3f',
    password: 'Bsmh.7700',
});


app.listen(PUERTO, () => {
    console.log(`Servidor compilado desde el puerto ${PUERTO}`);
});

conexion.connect((error) => {
    if (error) throw error;
    console.log('Conexión exitosa a MySQL');
});

app.get('/', (req, res) => {
    res.send('Nuestra API está casi funcionando');
});


async function recibirYProcesarComandos() {
    const connection = await amqp.connect(rabbitMqURL);
    const channel = await connection.createChannel();

    // Asegúrate de que el exchange esté declarado correctamente
    channel.assertExchange(exchangeName, 'direct', { durable: true });

    // Asegúrate de que la cola esté declarada correctamente
    channel.assertQueue(queueName, { durable: true });

    // Asegúrate de que la cola esté vinculada al exchange con la routing key adecuada
    channel.bindQueue(queueName, exchangeName, routingKey);

    // ...

    channel.consume(queueName, async (msg) => {
        const comando = JSON.parse(msg.content.toString());

        try {
            const operacion = comando.operacion;

            if (operacion) {  // Verificar si la propiedad 'operacion' está definida
                switch (operacion) {
                    case 'mysql':
                        await realizarOperacionMySQL(comando);
                        break;
                    case 'mongodb':
                        await realizarOperacionMongoDB(comando);
                        break;
                    case 'mysql_reserva':
                        await realizarOperacionMySQL(comando);
                        break;
                    case 'mongodb_reserva':
                        await realizarOperacionMongoDB(comando);
                        break;
                    default:
                        console.warn('Operación no reconocida. Ignorando:', operacion);
                    // Aquí puedes tomar alguna acción adicional si es necesario
                }
            } else {
                console.warn('Operación no definida en el comando. Ignorando el comando:', comando);
            }
        } catch (error) {
            console.error('Error al procesar el comando:', error);
        }
    }, { noAck: true });
}


// Iniciar la recepción y procesamiento de comandos
recibirYProcesarComandos().catch(console.error);


// Función para enviar comandos a RabbitMQ


// Función para enviar mensajes de escritura a RabbitMQ


// Función para publicar mensajes en RabbitMQ
async function publicarMensajeDeEscritura(comando) {
    const connection = await amqp.connect(rabbitMqURL);
    const channel = await connection.createChannel();

    const exchangeName = 'escritura_exchange';
    const queueName = 'escritura_queue';

    channel.assertExchange(exchangeName, 'direct', { durable: true });
    channel.assertQueue(queueName, { durable: true });
    channel.bindQueue(queueName, exchangeName, 'escritura');

    channel.publish(exchangeName, 'escritura', Buffer.from(JSON.stringify(comando)));
}

async function enviarMensajeDeEscrituraMySQL(comando) {
    await publicarMensajeDeEscritura(comando);
    const connection = await amqp.connect(rabbitMqURL);
    const channel = await connection.createChannel();

    const exchangeName = 'escritura_exchange';
    const queueName = 'escritura_queue';

    channel.assertExchange(exchangeName, 'direct', { durable: true });
    channel.assertQueue(queueName, { durable: true });
    channel.bindQueue(queueName, exchangeName, 'escritura');

    channel.publish(exchangeName, 'escritura', Buffer.from(JSON.stringify(comando)));
}

async function enviarMensajeDeEscrituraMongo(comando) {
    const connection = await amqp.connect(rabbitMqURL);
    const channel = await connection.createChannel();

    const exchangeName = 'escritura_exchange';
    const queueName = 'escritura_queue';

    channel.assertExchange(exchangeName, 'direct', { durable: true });
    channel.assertQueue(queueName, { durable: true });
    channel.bindQueue(queueName, exchangeName, 'escritura');

    channel.publish(exchangeName, 'escritura', Buffer.from(JSON.stringify(comando)));
}

async function realizarOperacionMySQL(comando) {
    console.log('Comando recibido:', comando);
    const conexionMySQL = mysql.createConnection({
        host: 'db4free.net',
        database: 'bd_brandon',
        user: 'herrera3f',
        password: 'Bsmh.7700',
    });

    try {
        await new Promise((resolve, reject) => {
            conexionMySQL.connect((error) => {
                if (error) {
                    reject(error);
                } else {
                    resolve();
                }
            });
        });

        if (comando.operacion === 'mysql_reserva') {
            const usuario_rut = comando.ID_Cliente; // Nuevo campo para el Rut del usuario
            const ID_Vuelos = comando.ID_Vuelos;

            // Verifica si la reserva ya existe en la base de datos
            const reservaExistente = await new Promise((resolve, reject) => {
                const sql = 'SELECT * FROM reserva WHERE `ID_Reserva` = ? AND `ID_Cliente` = ?'; // Ajusta según tu modelo
                conexionMySQL.query(sql, [comando.campo_uniqueness, usuario_rut], (error, results) => {
                    if (error) {
                        reject(error);
                    } else {
                        resolve(results.length > 0 ? results[0] : null);
                    }
                });
            });

            if (!reservaExistente) {
                // La reserva no existe, realiza una inserción
                const sql = 'INSERT INTO reserva (`ID_Vuelos`, `Nombre_Apellido`, Pais, `Numero_de_Documento`, `Fecha_de_Nacimiento`, Sexo, Email, Telefono, ID_Cliente) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)';
                const values = [comando.ID_Vuelos, comando['Nombre_Apellido'], comando.Pais, comando['Numero_de_Documento'], comando['Fecha_de_Nacimiento'], comando.Sexo, comando.Email, comando.Telefono, comando.ID_Cliente];




                console.log('Valores para la consulta SQL:', values);

                await new Promise((resolve, reject) => {
                    conexionMySQL.query(sql, values, (error) => {
                        if (error) {
                            reject(error);
                        } else {
                            console.log('Reserva agregada en MySQL.');
                            resolve();
                        }
                    });
                });
            }
        } else if (comando.operacion === 'mysql') {
            // Manejar la operación de registro de usuarios
            const clienteExistente = await new Promise((resolve, reject) => {
                const sql = 'SELECT * FROM clientes WHERE rut = ?';
                conexionMySQL.query(sql, [comando.rut], (error, results) => {
                    if (error) {
                        reject(error);
                    } else {
                        resolve(results.length > 0 ? results[0] : null);
                    }
                });
            });

            if (!clienteExistente) {
                // El cliente no existe, realiza una inserción
                const sql = 'INSERT INTO clientes (rut, nombre, email, contraseña) VALUES (?, ?, ?, ?)';
                const values = [comando.rut, comando.nombre, comando.email, comando.contraseña];

                await new Promise((resolve, reject) => {
                    conexionMySQL.query(sql, values, (error) => {
                        if (error) {
                            reject(error);
                        } else {
                            console.log('Cliente agregado en MySQL.');
                            resolve();
                        }
                    });
                });
            }
        } else {
            console.error('Operación no válida:', comando.operacion);
        }
    } catch (error) {
        console.error('Error al realizar operación en MySQL:', error);
    } finally {
        conexionMySQL.end();
    }
}

// Función para realizar operaciones en MongoDB
async function realizarOperacionMongoDB(comando) {
    console.log('Comando recibido:', comando);
    if (comando) {
        const mongoURI = 'mongodb+srv://benjaminmartinez29:Martinez890@User.bhz2ags.mongodb.net/sistema_reserva?retryWrites=true&w=majority';

        try {
            const conexionMongoDB = mongoose.createConnection(mongoURI, {
                useNewUrlParser: true,
                useUnifiedTopology: true,
            });
            console.log('Conexión a MongoDB establecida con éxito.');

            if (comando.operacion === 'mongodb') {
                const usuarioSchema = new mongoose.Schema({
                    rut: String,
                    nombre: String,
                    email: String,
                    contraseña: String,

                });

                const Usuario = conexionMongoDB.model('usuarios', usuarioSchema);

                if (comando.id) {
                    await Usuario.findByIdAndUpdate(comando.id, comando, { upsert: true });
                    console.log('Usuario actualizado en MongoDB.');
                } else {
                    await Usuario.create(comando);
                    console.log('Usuario agregado en MongoDB.');
                }
            } else if (comando.operacion === 'mongodb_reserva') {
                const usuario_rut = comando.usuario_rut; // Nuevo campo para el Rut del usuario

                const ReservaSchema = new mongoose.Schema({
                    usuario_rut: String, // Agrega el campo para el Rut del usuario
                    ID_Vuelos: String,
                    Nombre_Apellido: String,
                    Pais: String,
                    Numero_de_Documento: String,
                    Fecha_de_Nacimiento: String,
                    Sexo: String,
                    Email: String,
                    Telefono: String,

                });

                const Reserva = conexionMongoDB.model('Reserva', ReservaSchema);
                if (comando.id) {
                    await Reserva.findByIdAndUpdate(comando.id, comando, { upsert: true });
                    console.log('Reserva actualizada en MongoDB.');
                } else {
                    await Reserva.create(comando);
                    console.log('Reserva agregada en MongoDB.');
                }
            } else {
                console.error('Operación no válida:', comando.operacion);
            }

            // Publicar el mensaje, independientemente de la operación

        } catch (error) {
            console.error('Error al realizar operación en MongoDB:', error);
        } finally {
            conexionMongoDB.close();
        }
    }
}




app.post('/registro-mongodb-android', async (req, res) => {
    const comando = req.body;

    if (comando.operacion === 'mongodb') {
        const { operacion, rut, nombre, email, contraseña } = req.body;
        const mongoURI = 'mongodb+srv://benjaminmartinez29:Martinez890@User.bhz2ags.mongodb.net/sistema_reserva?retryWrites=true&w=majority';
        let conexionMongoDB;

        try {
            conexionMongoDB = mongoose.createConnection(mongoURI, {
                useNewUrlParser: true,
                useUnifiedTopology: true,
            });
            console.log('Conexión a MongoDB establecida con éxito.');

            const usuarioSchema = new mongoose.Schema({
                rut: String,
                nombre: String,
                email: String,
                contraseña: String,
            });

            const Usuario = conexionMongoDB.model('usuarios', usuarioSchema);

            await Usuario.create({ rut, nombre, email, contraseña });

            console.log('Usuario agregado en MongoDB (Android).');
            res.send('Registro en MongoDB (Android) realizado con éxito');
        } catch (error) {
            console.error('Error al realizar operación en MongoDB (Android):', error);
            res.status(500).send('Error al realizar operación en MongoDB (Android)');
        } finally {
            if (conexionMongoDB) {
                conexionMongoDB.close();
            }
        }
    } else {
        res.status(400).send('Operación no válida');
    }
});






app.post('/registro-sql-android', async (req, res) => {
    const comando = req.body;

    if (comando.operacion === 'sql') {
        const conexionMySQL = mysql.createConnection({
            host: 'db4free.net',
            database: 'bd_brandon',
            user: 'herrera3f',
            password: 'Bsmh.7700',
        });

        try {
            const clienteExistente = await new Promise((resolve, reject) => {
                const sql = 'SELECT * FROM clientes WHERE rut = ?';
                conexionMySQL.query(sql, [comando.rut], (error, results) => {
                    if (error) {
                        reject(error);
                    } else {
                        resolve(results.length > 0 ? results[0] : null);
                    }
                });
            });

            if (!clienteExistente) {
                // El cliente no existe, realiza una inserción
                const sql = 'INSERT INTO clientes (rut, nombre, email, contraseña) VALUES (?, ?, ?, ?)';
                const values = [comando.rut, comando.nombre, comando.email, comando.contraseña];

                await new Promise((resolve, reject) => {
                    conexionMySQL.query(sql, values, (error) => {
                        if (error) {
                            reject(error);
                        } else {
                            console.log('Cliente agregado en MySQL (Android).');
                            resolve();
                        }
                    });
                });
            }
            res.send('Registro en SQL (Android) realizado con éxito');
        } catch (error) {
            console.error('Error al realizar operación en MySQL (Android):', error);
            res.status(500).send('Error al realizar operación en MySQL (Android)');
        } finally {
            if (conexionMySQL) {
                conexionMySQL.end();
            }
        }
    } else {
        res.status(400).send('Operación no válida');
    }
});


app.post('/registrar-reserva-mysql-android', async (req, res) => {
    const comando = req.body;

    console.log('Recibiendo solicitud para registrar reserva en MySQL (Android):', comando);

    if (comando.operacion === 'mysql_reserva') {
        const conexionMySQL = mysql.createConnection({
            host: 'db4free.net',
            database: 'bd_brandon',
            user: 'herrera3f',
            password: 'Bsmh.7700',
        });

        try {
            await new Promise((resolve, reject) => {
                conexionMySQL.connect((error) => {
                    if (error) {
                        console.error('Error al conectar con MySQL:', error);
                        reject(error);
                    } else {
                        console.log('Conexión a MySQL establecida con éxito.');
                        resolve();
                    }
                });
            });

            // Eliminar la verificación de la existencia de la reserva por ID de vuelo
            // Comenta o elimina las siguientes líneas
            // const reservaExistente = await new Promise((resolve, reject) => {
            //     const sql = 'SELECT * FROM reserva WHERE `ID_Vuelos` = ?';
            //     conexionMySQL.query(sql, [comando.ID_Vuelos], (error, results) => {
            //         if (error) {
            //             console.error('Error al ejecutar la consulta de verificación en MySQL:', error);
            //             reject(error);
            //         } else {
            //             console.log('Consulta de verificación en MySQL ejecutada con éxito:', results);
            //             resolve(results.length > 0 ? results[0] : null);
            //         }
            //     });
            // });

            // Eliminar el bloque if (!reservaExistente) { ... }
            // Ya que no se está verificando la existencia de la reserva

            // Realiza la inserción directamente sin la verificación
            const sql = 'INSERT INTO reserva (`ID_Vuelos`, `Nombre_Apellido`, `Pais`, `Numero_de_Documento`, `Fecha_de_Nacimiento`, `Sexo`, `Email`, `Telefono`, `ID_Cliente`) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)';
            const values = [comando.ID_Vuelos, comando.Nombre_Apellido, comando.Pais, comando.Numero_de_Documento, comando.Fecha_de_Nacimiento, comando.Sexo, comando.Email, comando.Telefono, comando.ID_Cliente];

            await new Promise((resolve, reject) => {
                conexionMySQL.query(sql, values, (error, results) => {
                    if (error) {
                        console.error('Error al ejecutar la consulta de inserción en MySQL:', error);
                        reject(error);
                    } else {
                        console.log('Reserva agregada en MySQL (Android).');
                        resolve();
                    }
                });
            });

            res.send('Registro de reserva realizado con éxito');
        } catch (error) {
            console.error('Error al realizar operación de reserva en MySQL (Android):', error);
            res.status(500).send(`Error al realizar operación de reserva en MySQL (Android): ${error.message}`);
        } finally {
            if (conexionMySQL) {
                conexionMySQL.end();
                console.log('Conexión a MySQL cerrada con éxito.');
            }
        }
    } else {
        res.status(400).send('Operación no válida');
    }
});

// Define el esquema
const reservaSchema = new mongoose.Schema({
    usuario_rut: String,
    ID_Vuelos: String,
    Nombre_Apellido: String,
    Pais: String,
    Numero_de_Documento: String,
    Fecha_de_Nacimiento: String,
    Sexo: String,
    Email: String,
    Telefono: String
});

// Crea el modelo basado en el esquema
const Reserva = mongoose.model('Reserva', reservaSchema);

// Ruta para registrar reserva en MongoDB
app.post('/registrar-reserva-mongodb-android', async (req, res) => {
    const comando = req.body;
    console.log('Recibiendo solicitud para registrar reserva en MongoDB (Android):', comando);
    const mongoURI = 'mongodb+srv://benjaminmartinez29:Martinez890@User.bhz2ags.mongodb.net/sistema_reserva?retryWrites=true&w=majority';

    if (comando.operacion === 'mongodb_reserva') {
        const mongoURI = 'mongodb+srv://benjaminmartinez29:Martinez890@User.bhz2ags.mongodb.net/sistema_reserva?retryWrites=true&w=majority';

        try {
            // Conecta a MongoDB
            await mongoose.connect(mongoURI, {
                useNewUrlParser: true,
                useUnifiedTopology: true
            });

            console.log('Conexión a MongoDB establecida con éxito.');

            // Verifica si la reserva ya existe en la base de datos
            const reservaExistente = await Reserva.findOne({ ID_Vuelos: comando.ID_Vuelos, usuario_rut: comando.usuario_rut });

            if (!reservaExistente) {
                // La reserva no existe, realiza la inserción
                await Reserva.create({
                    ID_Vuelos: comando.ID_Vuelos,
                    usuario_rut: comando.rutUsuario,
                    Nombre_Apellido: comando.Nombre_Apellido,
                    Pais: comando.Pais,
                    Numero_de_Documento: comando.Numero_de_Documento,
                    Fecha_de_Nacimiento: comando.Fecha_de_Nacimiento,
                    Sexo: comando.Sexo,
                    Email: comando.Email,
                    Telefono: comando.Telefono,
                });

                console.log('Reserva agregada en MongoDB (Android).');
            }

            res.send('Registro de reserva realizado con éxito');
        } catch (error) {
            console.error('Error al realizar operación de reserva en MongoDB (Android):', error);
            res.status(500).send('Error al realizar operación de reserva en MongoDB (Android)');
        } finally {
            // Cierra la conexión después de realizar la operación
            mongoose.connection.close();
        }
    } else {
        res.status(400).send('Operación no válida');
    }
});


