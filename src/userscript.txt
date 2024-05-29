// ==UserScript==
// @name         BrokeCord Solver
// @version      0.1
// @description
// @match        https://*.discord.com/*
// @match        https://*.hcaptcha.com/*
// @grant        none
// ==/UserScript==

// Here is the fully released source code. To the skids: don't try to sell it, no one will buy and it's not upscalable.

(() => {
    'use strict';

    const Time = (() => {
        const sleep = (i = 1000) => {
            return new Promise((resolve) => setTimeout(resolve, i));
        };

        const random_sleep = async (min, max) => {
            const duration = Math.floor(Math.random() * (max - min) + min);
            return await sleep(duration);
        };

        const now = () => {
            if (!Date.now) {
                Date.now = () => new Date().getTime();
            }
            return Date.now();
        };

        return { sleep, random_sleep, now };
    })();

    const simulateMouseClick = (element, clientX = null, clientY = null) => {
        if (!element) {
            return;
        }
        const eventNames = [
            'mouseover',
            'mouseenter',
            'mousedown',
            'mouseup',
            'click',
            'mouseout',
        ];
        eventNames.forEach((eventName) => {
            const detail = eventName === 'mouseover' ? 0 : 1;
            const event = new MouseEvent(eventName, {
                detail: detail,
                view: window,
                bubbles: true,
                cancelable: true,
                clientX: null,
                clientY: null,
            });
            element.dispatchEvent(event);
        });
    };

    const get_task = async () => {
        await Time.sleep(3000);
        let menu = document.querySelector('#menu-info');
        simulateMouseClick(menu);
        let textChBtn = document.querySelector('#text_challenge');
        simulateMouseClick(textChBtn);
        let repeatCount = 1;
        while (repeatCount > 0) {
            for (let i = 0; i < 3; i++) {
                await Time.sleep(2000);
                let task = document.querySelector('h2.prompt-text#prompt')?.innerText?.replace(/\s+/g, ' ')?.trim();
                let task2 = document.querySelector('div.text-text#prompt-text')?.innerText?.replace(/\s+/g, ' ')?.trim();
                let fulltask = task + ": " + task2;
                const apiUrl = 'http://127.0.0.1:5000/api';
                if (task && task2) {
                    try {
                        let response = await fetch(apiUrl, {
                            method: 'POST',
                            headers: {
                                'Content-Type': 'application/json'
                            },
                            body: JSON.stringify({
                                fulltask: fulltask
                            })
                        });
                        let data = await response.json();
                        console.log('Question:', fulltask);
                        let input = document.querySelector('input[type="text"]');
                        simulateMouseClick(input);
                        const fix = (text) => {
                            let lowercaseString = text.toLowerCase();
                            let cleanedString = lowercaseString.replace(/[^a-zí]/g, '');
                            if (/(no|sí)$/.test(cleanedString)) {
                                return cleanedString;
                            } else {
                                return Math.random() < 0.5 ? 'no' : 'sí';
                            }
                        };
                        const fixedString = fix(data.answer);
                        let typeResponse = await fetch('http://127.0.0.1:5000/type', {
                            method: 'POST',
                            headers: {
                                'Content-Type': 'application/json',
                                'Access-Control-Allow-Origin': '*'
                            },
                            body: JSON.stringify({
                                fixedString: fixedString
                            })
                        });
                        let typeData = await typeResponse.json();
                        console.log(typeData);
                    } catch (error) {
                        console.error('Error calling API:', error);
                    }
                }
            }
            await Time.sleep(3000);
            if (is_notsolved()) {
                repeatCount = 1;
            } else {
                repeatCount = 0;
            }
        }
    };

    const submit = () => {
        try {
            simulateMouseClick(document.querySelector('.button-submit'));
        } catch (e) {
            console.error('Error submitting', e);
        }
    };

    const on_widget_frame = async () => {
        await Time.sleep(500);
        await open_image_frame();
    };

    const on_image_frame = async () => {
        if (document.querySelector('.display-language .text')) {
            simulateMouseClick(
                document.querySelector('.language-selector .option:nth-child(90)')
            );
            await Time.sleep(500);
        }
        await get_task();
    };

    const is_widget_frame = () => {
        return new Promise(resolve => {
            const interval = setInterval(() => {
                const iframe = document.querySelector('iframe[src*="newassets.hcaptcha.com"]');
                if (iframe) {
                    clearInterval(interval);
                    resolve(true);
                }
            }, 500);
        });
    };

    const is_image_frame = () => {
        return document.querySelector('h2.prompt-text') !== null;
    };

    const open_image_frame = async () => {
        simulateMouseClick(document.querySelector('#anchor'));
        await Time.sleep(1000);
        if (is_image_frame()) {
            await on_image_frame();
        }
    };

    const is_notsolved = () => {
        const errorText = document.querySelector('div.error-text');
        return errorText && (errorText.innerText.includes('Inténtalo de nuevo') || errorText.innerText.includes('⚠️'));
    };

    (async () => {
        await Time.sleep(1000);
        if (is_widget_frame()) {
             on_widget_frame();
        }
    })();
})();
