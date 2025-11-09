import { Db, MongoClient } from 'mongodb';

// Ensure you have MONGODB_URI in your .env.local file
const uri: string|undefined = process.env.MONGODB_URI;
const dbName = process.env.MONGODB_DB_NAME || 'your-default-db-name';

if (!uri) {
  throw new Error('Please define the MONGODB_URI environment variable inside .env.local');
}

let cachedClient: MongoClient | null = null;
let cachedDb: Db | null = null;

export async function connectToDb() {
  if (cachedClient && cachedDb) {
    return { client: cachedClient, db: cachedDb };
  }

  if (!uri) {
    throw new Error('Please define the MONGODB_URI environment variable inside .env.local');
  }

  const client = new MongoClient(uri);

  try {
    await client.connect();
    const db = client.db(dbName);

    cachedClient = client;
    cachedDb = db;

    console.log("Connected to MongoDB");
    return { client, db };
  } catch (error) {
    console.error("Failed to connect to MongoDB", error);
    // Gracefully handle connection error, maybe by closing the client
    await client.close();
    throw error;
  }
}
type createVideoPromptInput = {
    userid: string;
    prompt: string;
}
export async function createVideoPrompt(promptData: createVideoPromptInput) {
  // 1. Validate input data (basic example)
  if (!promptData.userid || !promptData.prompt) {
    return { 
      success: false,
      error: 'User ID and prompt are required.'
    };
  }

  let db;
  try {
    // 2. Connect to the database
    // The connectToDb function handles connection logic
    ({ db } = await connectToDb());
  } catch (error) {
    console.error('Database connection error:', error);
    return {
      success: false,
      error: 'Failed to connect to the database.'
    };
  }

  try {
    // 3. Get the collection and insert the document
    const collection = db.collection('videoPrompts'); // Or your preferred collection name

    // Add a timestamp for good measure
    const documentToInsert = {
      ...promptData,
      status: 'pending', // Initial status
      createdAt: new Date(),
    };

    const result = await collection.insertOne(documentToInsert);

    // 4. (Optional) Revalidate a path if a page needs to show the new data
    // For example, if you have a dashboard at '/dashboard'
    // revalidatePath('/dashboard');

    console.log('Document-ID ' + result.insertedId + ' inserted in ' + collection.collectionName);

    // 5. Return a success response
    return {
      success: true,
      data: { insertedId: result.insertedId },
    };

  } catch (error) {
    console.error('Database insertion error:', error);
    return {
      success: false,
      error: 'Failed to create the document.'
    };
  }
  
  // Note: The 'client' from connectToDb doesn't need to be explicitly closed here
  // because we are caching the connection. If you weren't caching,
  // you would use a try...finally block to ensure client.close() is called.
}
