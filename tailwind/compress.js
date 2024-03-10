import * as zlib from "zlib";
import * as fs from "fs";

console.log("compressing...");
const args = process.argv;
if (args.length === 3) {
    const inputFile = args[2];
    compress(inputFile);
}

async function compress(inputFile) {
    // Create temporary file name
    const outputFile = inputFile + '.br';

    try {
        // Create Brotli compression stream
        const brotliStream = zlib.createBrotliCompress({
            chunkSize: 32 * 1024,
            params: {
                [zlib.constants.BROTLI_PARAM_MODE]: zlib.constants.BROTLI_MODE_TEXT,
                [zlib.constants.BROTLI_PARAM_QUALITY]: 4,
                [zlib.constants.BROTLI_PARAM_SIZE_HINT]: fs.statSync(inputFile).size,
            },
        });

        // Create read and write streams
        const readStream = fs.createReadStream(inputFile);
        const writeStream = fs.createWriteStream(outputFile);

        // Pipe data, compress, and write to temporary file
        await new Promise((resolve, reject) => {
            readStream.pipe(brotliStream).pipe(writeStream).on('finish', resolve).on('error', reject);
        });

        console.log('Successfully compressed and replaced:', inputFile);
    } catch (err) {
        console.error('Error during compression or replacement:', err);

        // Optional: Clean up temporary file if creation failed
        if (fs.existsSync(outputFile)) {
            await fs.promises.unlink(outputFile);
        }
    }
}