// Customized code copy button
document.addEventListener('DOMContentLoaded', () => {
  const copyButtons = document.querySelectorAll('.copy-code');

  copyButtons.forEach((button) => {
    button.addEventListener('click', () => {
      const codeBlock = button.parentNode.querySelector('code');
      let code = codeBlock.innerText;
      
      // For bash/shell/zsh commands, remove the $ prompt if present
      if (button.parentNode.classList.contains('language-bash') || 
          button.parentNode.classList.contains('language-shell') ||
          button.parentNode.classList.contains('language-zsh')) {
        code = code.replace(/^\$ /gm, '');
      }

      navigator.clipboard.writeText(code).then(() => {
        button.innerText = 'Copied!';
        setTimeout(() => {
          button.innerText = 'Copy';
        }, 2000);
      }).catch((error) => {
        console.error('Failed to copy code:', error);
        button.innerText = 'Error!';
        setTimeout(() => {
          button.innerText = 'Copy';
        }, 2000);
      });
    });
  });
});