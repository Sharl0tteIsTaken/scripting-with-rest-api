// template by @Roshanjossey in:
// https://github.com/firstcontributions/first-contributions/pull/106342#issuecomment-3507142666

import axios from 'axios';
import dotenv from 'dotenv';
import { fileURLToPath } from 'url';
import { dirname, join } from 'path';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);
dotenv.config({ path: join(__dirname, '.env') });

// Replace with your GitHub Personal Access Token
const GITHUB_TOKEN = process.env.GITHUB_TOKEN;
const HEADERS = { Authorization: `token ${GITHUB_TOKEN}` };


async function createIssue(options) {
  const { repo, title, body, labels } = options;
  
  // For testing, just log what would be created instead of actually creating
  console.log(`Issue would be created: ${title}`);
  
  // Uncomment the following lines to actually create issues
  // const url = `https://api.github.com/repos/${repo}/issues`;

  // try {
  //   const response = await axios.post(
  //     url,
  //     { title, body, labels },
  //     { headers: HEADERS }
  //   );
  //   console.log(`Issue created: ${response.data.html_url}`);
  // } catch (error) {
  //   console.error(`Error creating issue "${title}":`, error.response?.data || error.message);
  // }
}

async function main(repo, languages) {

  const labels = ['documentation', 'help wanted', 'good first issue', 'enhancement'];

  for (const language of languages) {
    const body = `
    🎯 **Goal**
Replace the character used for angle brackets within HTML `<pre>` tag in the ${language.name} translation of README to properly display the error message.

🐞 **Problem**
The ${language.name} translation [\`${language.chapter}\`]() section, in the first code block in the collapsible section (**\`${language.summary}\`**), the last line uses the character \`<\` within an HTML \`<pre>\` tag, causing \`<your-username>\` to be treated as an HTML tag and therefore invisible.

💡 **What needs to be done**
Replace the angle brackets within HTML `<pre>` tag with [HTML character reference](https://developer.mozilla.org/en-US/docs/Glossary/Character_reference). You can find the file to work on at the following URL:
${language.filepath}

🔧**What needs to be changed**
- Locate the line begin with: \`fatal: Authentication failed for 'https://github.com/...'\`
- Replace \`<\` with \`&lt;\` in this line
- Replace \`>\` with \`&gt;\` in this line

🗺️ **Example of what needs to be fixed**
> - Authentication Error (On the ${language.name} translation)
> remote: Support for password authentication was removed on August 13, 2021. Please use a personal access token instead.
> remote: Please see https://github.blog/2020-12-15-token-authentication-requirements-for-git-operations/ for more information.
> fatal: Authentication failed for 'https://github.com//first-contributions.git/'

> - Authentication Error (After the replacement)
> remote: Support for password authentication was removed on August 13, 2021. Please use a personal access token instead.
> remote: Please see https://github.blog/2020-12-15-token-authentication-requirements-for-git-operations/ for more information.
> fatal: Authentication failed for 'https://github.com/&lt;your-username&gt;/first-contributions.git/'

> - Authentication Error (How it should be displayed)
> remote: Support for password authentication was removed on August 13, 2021. Please use a personal access token instead.
> remote: Please see https://github.blog/2020-12-15-token-authentication-requirements-for-git-operations/ for more information.
> fatal: Authentication failed for '[https://github.com/<your-username\>/first-contributions.git/](https://github.com/<your-username>/first-contributions.git/)'

> [!Important]
> Please only address one issue in a PR.
> Let's make it possible for more people to solve issues here.

📋 **Steps to solve the problem**
- Comment below about what you've started working on.
- Find the line starting with: \`fatal: Authentication failed for 'https://github.com/...'\`
- Replace the angle brackets
- Ensure core block display angle brackets properly
- Add, commit, push your changes.
- Submit a pull request and add this in comments - 'Resolves #'
- Ask for reviews in comments section of pull request.
- Celebrate your contribution to this project. 🎉
    `;
    const title = `Fix angle brackets within HTML <pre> tag in ${language.name} translation`;
    await createIssue({ repo, title, body, labels });
  }
}


const [repo, languages] = ['firstcontributions/first-contributions', [
  {
    name: 'French',
    code: 'fr',
    filepath: 'https://github.com/firstcontributions/first-contributions/blob/main/docs/translations/README.fr.md',
    chapter: '',
    summary: '',
  },
  {
    name: 'Assamese',
    code: 'assamese',
    filepath: 'https://github.com/firstcontributions/first-contributions/blob/main/docs/translations/README.assamese.md',
  },
]]
main(repo, languages).catch((error) => {
  console.error('Error:', error.message);
});
