const tl = require('azure-pipelines-task-lib/task');
const cp = require('child_process');

async function run() {
    try {
        const schemaPath = tl.getPathInput('schemaPath', true, true);
        const minScore = tl.getInput('minScore', false) || '75.0';
        const compileOutput = tl.getInput('compileOutput', false);

        console.log(`[SemanticFlow] Iniciando validación de calidad semántica en: ${schemaPath}`);
        console.log(`[SemanticFlow] Umbral mínimo cQS: ${minScore}`);

        // 1. Ejecutar validación
        const validateCmd = `semanticflow validate --input "${schemaPath}" --min-score "${minScore}"`;
        console.log(`[SemanticFlow] Ejecutando: ${validateCmd}`);
        
        try {
            cp.execSync(validateCmd, { stdio: 'inherit' });
            tl.setResult(tl.TaskResult.Succeeded, 'Modelo semántico cumple el Quality Gate cQS satisfactoriamente.');
        } catch (error) {
            tl.setResult(tl.TaskResult.Failed, `Fallo en el Quality Gate de SemanticFlow: El modelo no alcanza el umbral de ${minScore} o contiene errores críticos.`);
            return;
        }

        // 2. Si se solicitó compilación, emitir artefactos
        if (compileOutput) {
            console.log(`[SemanticFlow] Compilando modelo hacia: ${compileOutput}`);
            const compileCmd = `semanticflow compile --input "${schemaPath}" --output "${compileOutput}" --name "AzureDevOpsModel"`;
            cp.execSync(compileCmd, { stdio: 'inherit' });
        }
    } catch (err) {
        tl.setResult(tl.TaskResult.Failed, err.message);
    }
}

run();
