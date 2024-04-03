import * as esbuild from "esbuild";
import stylePlugin from "esbuild-style-plugin";
import tailwindcss from "tailwindcss";
import autoprefixer from "autoprefixer";
import chokidar from "chokidar";
import cssnanoPlugin from "cssnano";

const enableWatch = process.argv.some(a => a === "--watch");
const enableAnalyze = process.argv.some(a => a === "--analyze");

const ctx = await esbuild.context({
    entryPoints: [
        "src/*.ts"
    ],
    outdir: "../static/compiled/",
    bundle: true,
    minify: true,
    sourcemap: true,
    treeShaking: true,
    metafile: enableAnalyze,
    plugins: [stylePlugin({
        postcss: {
            plugins: [tailwindcss, autoprefixer, cssnanoPlugin]
        }
    })],
});

const doBuild = async () => {
    try {
        const build = await ctx.rebuild();
        if (enableAnalyze) {
            console.log(await esbuild.analyzeMetafile(build.metafile, {
                color: true, verbose: false
            }));
        }
    } catch (e) {
        console.error(e);
    }
}

if (enableWatch) {
    const watcher = chokidar.watch([
        "src/**/*.{ts,css}",
        "../**/*.html",
        "!../.venv/**/*",
        "!../venv/**/*",
        "!node_modules/**/*",
    ], {
        persistent: true
    });
    watcher.on("change", async path => {
        console.log(`Detected changed in: ${path}`);
        await doBuild();
    });
    console.log("Initial build...");
    await doBuild();
    console.log("Watching...");
} else {
    await doBuild();
    await ctx.dispose();
}
