=============
 darkgraylib
=============

|build-badge| |license-badge| |pypi-badge| |downloads-badge| |black-badge| |changelog-badge|

.. |build-badge| image:: https://github.com/akaihola/darkgraylib/actions/workflows/python-package.yml/badge.svg
   :alt: main branch build status
   :target: https://github.com/akaihola/darkgraylib/actions/workflows/python-package.yml?query=branch%3Amain
.. |license-badge| image:: https://img.shields.io/badge/License-BSD%203--Clause-blue.svg
   :alt: BSD 3 Clause license
   :target: https://github.com/akaihola/darkgraylib/blob/main/LICENSE
.. |pypi-badge| image:: https://img.shields.io/pypi/v/darkgraylib
   :alt: Latest release on PyPI
   :target: https://pypi.org/project/darkgraylib/
.. |downloads-badge| image:: https://pepy.tech/badge/darkgraylib
   :alt: Number of downloads
   :target: https://pepy.tech/project/darkgraylib
.. |black-badge| image:: https://img.shields.io/badge/code%20style-black-000000.svg
   :alt: Source code formatted using Black
   :target: https://github.com/psf/black
.. |changelog-badge| image:: https://img.shields.io/badge/-change%20log-purple
   :alt: Change log
   :target: https://github.com/akaihola/darkgraylib/blob/main/CHANGES.rst
.. |next-milestone| image:: https://img.shields.io/github/milestones/progress/akaihola/darkgraylib/8?color=red&label=release%201.3.1
   :alt: Next milestone
   :target: https://github.com/akaihola/darkgraylib/milestone/4


What?
=====

This package is a placeholder for common supporting code for Darker_ and Graylint_.

Such pieces of code have been moved from Darker_ to this new package.

.. _Darker: https://pypi.org/project/darker
.. _Graylint: https://pypi.org/project/graylint

+------------------------------------------------+--------------------------------+
| |you-can-help|                                 | |support|                      |
+================================================+================================+
| We're asking the community kindly for help to  | We have a                      |
| review pull requests for |next-milestone|.     | `community support channel`_   |
| If you have a moment to spare, please take a   | on GitHub Discussions. Welcome |
| look at one of them and shoot us a comment!    | to ask for help and advice!    |
+------------------------------------------------+--------------------------------+

.. |you-can-help| image:: https://img.shields.io/badge/-You%20can%20help-green?style=for-the-badge
   :alt: You can help
.. |support| image:: https://img.shields.io/badge/-Support-green?style=for-the-badge
   :alt: Support
.. _#151: https://github.com/akaihola/darker/issues/151
.. _community support channel: https://github.com/akaihola/darker/discussions


Why?
====

Darker_ and Graylint_ originate from the same original Darker_ code base. In February
2023, linter support was decided to be moved out from Darker_. Obviously, the two tools
are still very similar and share a lot of under-the-hood functionality. For maintenance
purposes, those common pieces are being moved into this package.


License
=======

BSD. See ``LICENSE``.


Contributors ✨
===============

Thanks goes to these wonderful people (`emoji key`_):

.. raw:: html

   <!-- ALL-CONTRIBUTORS-LIST:START - Do not remove or modify this section
        This is automatically generated. Please update `contributors.yaml` and
        see `CONTRIBUTING.rst` for how to re-generate this table. -->
   <table>
     <tr>
       <td align="center">
         <a href="https://github.com/wnoise">
           <img src="https://avatars.githubusercontent.com/u/9107?v=3" width="100px;" alt="@wnoise" />
           <br />
           <sub>
             <b>Aaron Denney</b>
           </sub>
         </a>
         <br />
         <a href="https://github.com/search?q=repo%3Aakaihola%2Fdarkgraylib+repo%3Aakaihola%2Fdarker+author%3Awnoise&type=issues" title="Bug reports">🐛</a>
       </td>
       <td align="center">
         <a href="https://github.com/agandra">
           <img src="https://avatars.githubusercontent.com/u/1072647?v=3" width="100px;" alt="@agandra" />
           <br />
           <sub>
             <b>Aditya Gandra</b>
           </sub>
         </a>
         <br />
         <a href="https://github.com/search?q=repo%3Aakaihola%2Fdarkgraylib+repo%3Aakaihola%2Fdarker+author%3Aagandra&type=issues" title="Bug reports">🐛</a>
       </td>
       <td align="center">
         <a href="https://github.com/aljazerzen">
           <img src="https://avatars.githubusercontent.com/u/11072061?v=3" width="100px;" alt="@aljazerzen" />
           <br />
           <sub>
             <b>Aljaž Mur Eržen</b>
           </sub>
         </a>
         <br />
         <a href="https://github.com/search?q=repo%3Aakaihola%2Fdarkgraylib+repo%3Aakaihola%2Fdarker+author%3Aaljazerzen&type=commits" title="Code">💻</a>
       </td>
       <td align="center">
         <a href="https://github.com/akaihola">
           <img src="https://avatars.githubusercontent.com/u/13725?v=3" width="100px;" alt="@akaihola" />
           <br />
           <sub>
             <b>Antti Kaihola</b>
           </sub>
         </a>
         <br />
         <a href="https://github.com/search?q=repo%3Aakaihola%2Fdarkgraylib+repo%3Aakaihola%2Fdarker+akaihola" title="Answering Questions">💬</a>
         <a href="https://github.com/search?q=repo%3Aakaihola%2Fdarkgraylib+repo%3Aakaihola%2Fdarker+author%3Aakaihola&type=commits" title="Code">💻</a>
         <a href="https://github.com/search?q=repo%3Aakaihola%2Fdarkgraylib+repo%3Aakaihola%2Fdarker+author%3Aakaihola&type=commits" title="Documentation">📖</a>
         <a href="https://github.com/search?q=repo%3Aakaihola%2Fdarkgraylib+repo%3Aakaihola%2Fdarker+reviewed-by%3Aakaihola&type=pullrequests" title="Reviewed Pull Requests">👀</a>
         <a href="https://github.com/search?q=repo%3Aakaihola%2Fdarkgraylib+repo%3Aakaihola%2Fdarker+author%3Aakaihola&type=commits" title="Maintenance">🚧</a>
       </td>
       <td align="center">
         <a href="https://github.com/levouh">
           <img src="https://avatars.githubusercontent.com/u/31262046?v=3" width="100px;" alt="@levouh" />
           <br />
           <sub>
             <b>August Masquelier</b>
           </sub>
         </a>
         <br />
         <a href="https://github.com/search?q=repo%3Aakaihola%2Fdarkgraylib+repo%3Aakaihola%2Fdarker+author%3Alevouh&type=pullrequests" title="Code">💻</a>
         <a href="https://github.com/search?q=repo%3Aakaihola%2Fdarkgraylib+repo%3Aakaihola%2Fdarker+author%3Alevouh&type=issues" title="Bug reports">🐛</a>
       </td>
       <td align="center">
         <a href="https://github.com/AckslD">
           <img src="https://avatars.githubusercontent.com/u/23341710?v=3" width="100px;" alt="@AckslD" />
           <br />
           <sub>
             <b>Axel Dahlberg</b>
           </sub>
         </a>
         <br />
         <a href="https://github.com/search?q=repo%3Aakaihola%2Fdarkgraylib+repo%3Aakaihola%2Fdarker+author%3AAckslD&type=issues" title="Bug reports">🐛</a>
       </td>
     </tr>
     <tr>
       <td align="center">
         <a href="https://github.com/qubidt">
           <img src="https://avatars.githubusercontent.com/u/6306455?v=3" width="100px;" alt="@qubidt" />
           <br />
           <sub>
             <b>Bao</b>
           </sub>
         </a>
         <br />
         <a href="https://github.com/search?q=repo%3Aakaihola%2Fdarkgraylib+repo%3Aakaihola%2Fdarker+author%3Aqubidt&type=issues" title="Bug reports">🐛</a>
       </td>
       <td align="center">
         <a href="https://github.com/falkben">
           <img src="https://avatars.githubusercontent.com/u/653031?v=3" width="100px;" alt="@falkben" />
           <br />
           <sub>
             <b>Ben Falk</b>
           </sub>
         </a>
         <br />
         <a href="https://github.com/search?q=repo%3Aakaihola%2Fdarkgraylib+repo%3Aakaihola%2Fdarker+author%3Afalkben&type=pullrequests" title="Documentation">📖</a>
       </td>
       <td align="center">
         <a href="https://github.com/brtknr">
           <img src="https://avatars.githubusercontent.com/u/2181426?v=3" width="100px;" alt="@brtknr" />
           <br />
           <sub>
             <b>Bharat Kunwar</b>
           </sub>
         </a>
         <br />
         <a href="https://github.com/search?q=repo%3Aakaihola%2Fdarkgraylib+repo%3Aakaihola%2Fdarker+reviewed-by%3Abrtknr&type=pullrequests" title="Reviewed Pull Requests">👀</a>
       </td>
       <td align="center">
         <a href="https://github.com/casio">
           <img src="https://avatars.githubusercontent.com/u/29784?v=3" width="100px;" alt="@casio" />
           <br />
           <sub>
             <b>Carsten Kraus</b>
           </sub>
         </a>
         <br />
         <a href="https://github.com/search?q=repo%3Aakaihola%2Fdarkgraylib+repo%3Aakaihola%2Fdarker+author%3Acasio&type=issues" title="Bug reports">🐛</a>
       </td>
       <td align="center">
         <a href="https://github.com/chmouel">
           <img src="https://avatars.githubusercontent.com/u/98980?v=3" width="100px;" alt="@chmouel" />
           <br />
           <sub>
             <b>Chmouel Boudjnah</b>
           </sub>
         </a>
         <br />
         <a href="https://github.com/search?q=repo%3Aakaihola%2Fdarkgraylib+repo%3Aakaihola%2Fdarker+author%3Achmouel&type=pullrequests" title="Code">💻</a>
         <a href="https://github.com/search?q=repo%3Aakaihola%2Fdarkgraylib+repo%3Aakaihola%2Fdarker+author%3Achmouel&type=issues" title="Bug reports">🐛</a>
       </td>
       <td align="center">
         <a href="https://github.com/cclauss">
           <img src="https://avatars.githubusercontent.com/u/3709715?v=3" width="100px;" alt="@cclauss" />
           <br />
           <sub>
             <b>Christian Clauss</b>
           </sub>
         </a>
         <br />
         <a href="https://github.com/search?q=repo%3Aakaihola%2Fdarkgraylib+repo%3Aakaihola%2Fdarker+author%3Acclauss&type=pullrequests" title="Code">💻</a>
       </td>
     </tr>
     <tr>
       <td align="center">
         <a href="https://github.com/chrisdecker1201">
           <img src="https://avatars.githubusercontent.com/u/20707614?v=3" width="100px;" alt="@chrisdecker1201" />
           <br />
           <sub>
             <b>Christian Decker</b>
           </sub>
         </a>
         <br />
         <a href="https://github.com/search?q=repo%3Aakaihola%2Fdarkgraylib+repo%3Aakaihola%2Fdarker+author%3Achrisdecker1201&type=pullrequests" title="Code">💻</a>
         <a href="https://github.com/search?q=repo%3Aakaihola%2Fdarkgraylib+repo%3Aakaihola%2Fdarker+author%3Achrisdecker1201&type=issues" title="Bug reports">🐛</a>
       </td>
       <td align="center">
         <a href="https://github.com/KangOl">
           <img src="https://avatars.githubusercontent.com/u/38731?v=3" width="100px;" alt="@KangOl" />
           <br />
           <sub>
             <b>Christophe Simonis</b>
           </sub>
         </a>
         <br />
         <a href="https://github.com/search?q=repo%3Aakaihola%2Fdarkgraylib+repo%3Aakaihola%2Fdarker+author%3AKangOl&type=issues" title="Bug reports">🐛</a>
       </td>
       <td align="center">
         <a href="https://github.com/CorreyL">
           <img src="https://avatars.githubusercontent.com/u/16601729?v=3" width="100px;" alt="@CorreyL" />
           <br />
           <sub>
             <b>Correy Lim</b>
           </sub>
         </a>
         <br />
         <a href="https://github.com/search?q=repo%3Aakaihola%2Fdarkgraylib+repo%3Aakaihola%2Fdarker+author%3ACorreyL&type=commits" title="Code">💻</a>
         <a href="https://github.com/search?q=repo%3Aakaihola%2Fdarkgraylib+repo%3Aakaihola%2Fdarker+author%3ACorreyL&type=commits" title="Documentation">📖</a>
         <a href="https://github.com/search?q=repo%3Aakaihola%2Fdarkgraylib+repo%3Aakaihola%2Fdarker+reviewed-by%3ACorreyL&type=pullrequests" title="Reviewed Pull Requests">👀</a>
       </td>
       <td align="center">
         <a href="https://github.com/fizbin">
           <img src="https://avatars.githubusercontent.com/u/4110350?v=3" width="100px;" alt="@fizbin" />
           <br />
           <sub>
             <b>Daniel Martin</b>
           </sub>
         </a>
         <br />
         <a href="https://github.com/search?q=repo%3Aakaihola%2Fdarkgraylib+repo%3Aakaihola%2Fdarker+author%3Afizbin&type=issues" title="Bug reports">🐛</a>
       </td>
       <td align="center">
         <a href="https://github.com/DavidCDreher">
           <img src="https://avatars.githubusercontent.com/u/47252106?v=3" width="100px;" alt="@DavidCDreher" />
           <br />
           <sub>
             <b>David Dreher</b>
           </sub>
         </a>
         <br />
         <a href="https://github.com/search?q=repo%3Aakaihola%2Fdarkgraylib+repo%3Aakaihola%2Fdarker+author%3ADavidCDreher&type=issues" title="Bug reports">🐛</a>
       </td>
       <td align="center">
         <a href="https://github.com/shangxiao">
           <img src="https://avatars.githubusercontent.com/u/1845938?v=3" width="100px;" alt="@shangxiao" />
           <br />
           <sub>
             <b>David Sanders</b>
           </sub>
         </a>
         <br />
         <a href="https://github.com/search?q=repo%3Aakaihola%2Fdarkgraylib+repo%3Aakaihola%2Fdarker+author%3Ashangxiao&type=pullrequests" title="Code">💻</a>
         <a href="https://github.com/search?q=repo%3Aakaihola%2Fdarkgraylib+repo%3Aakaihola%2Fdarker+author%3Ashangxiao&type=issues" title="Bug reports">🐛</a>
       </td>
     </tr>
     <tr>
       <td align="center">
         <a href="https://github.com/dhrvjha">
           <img src="https://avatars.githubusercontent.com/u/43818577?v=3" width="100px;" alt="@dhrvjha" />
           <br />
           <sub>
             <b>Dhruv Kumar Jha</b>
           </sub>
         </a>
         <br />
         <a href="https://github.com/search?q=repo%3Aakaihola%2Fdarkgraylib+repo%3Aakaihola%2Fdarker+commenter%3Adhrvjha&type=issues" title="Bug reports">🐛</a>
         <a href="https://github.com/search?q=repo%3Aakaihola%2Fdarkgraylib+repo%3Aakaihola%2Fdarker+author%3Adhrvjha&type=pullrequests" title="Code">💻</a>
       </td>
       <td align="center">
         <a href="https://github.com/k-dominik">
           <img src="https://avatars.githubusercontent.com/u/24434157?v=3" width="100px;" alt="@k-dominik" />
           <br />
           <sub>
             <b>Dominik Kutra</b>
           </sub>
         </a>
         <br />
         <a href="https://github.com/search?q=repo%3Aakaihola%2Fdarkgraylib+repo%3Aakaihola%2Fdarker+commenter%3Ak-dominik&type=issues" title="Bug reports">🐛</a>
       </td>
       <td align="center">
         <a href="https://github.com/virtuald">
           <img src="https://avatars.githubusercontent.com/u/567900?v=3" width="100px;" alt="@virtuald" />
           <br />
           <sub>
             <b>Dustin Spicuzza</b>
           </sub>
         </a>
         <br />
         <a href="https://github.com/search?q=repo%3Aakaihola%2Fdarkgraylib+repo%3Aakaihola%2Fdarker+author%3Avirtuald&type=issues" title="Bug reports">🐛</a>
       </td>
       <td align="center">
         <a href="https://github.com/DylanYoung">
           <img src="https://avatars.githubusercontent.com/u/5795220?v=3" width="100px;" alt="@DylanYoung" />
           <br />
           <sub>
             <b>DylanYoung</b>
           </sub>
         </a>
         <br />
         <a href="https://github.com/search?q=repo%3Aakaihola%2Fdarkgraylib+repo%3Aakaihola%2Fdarker+author%3ADylanYoung&type=issues" title="Bug reports">🐛</a>
       </td>
       <td align="center">
         <a href="https://github.com/phitoduck">
           <img src="https://avatars.githubusercontent.com/u/32227767?v=3" width="100px;" alt="@phitoduck" />
           <br />
           <sub>
             <b>Eric Riddoch</b>
           </sub>
         </a>
         <br />
         <a href="https://github.com/search?q=repo%3Aakaihola%2Fdarkgraylib+repo%3Aakaihola%2Fdarker+author%3Aphitoduck&type=issues" title="Bug reports">🐛</a>
       </td>
       <td align="center">
         <a href="https://github.com/samoylovfp">
           <img src="https://avatars.githubusercontent.com/u/17025459?v=3" width="100px;" alt="@samoylovfp" />
           <br />
           <sub>
             <b>Filipp Samoilov</b>
           </sub>
         </a>
         <br />
         <a href="https://github.com/search?q=repo%3Aakaihola%2Fdarkgraylib+repo%3Aakaihola%2Fdarker+reviewed-by%3Asamoylovfp&type=pullrequests" title="Reviewed Pull Requests">👀</a>
       </td>
     </tr>
     <tr>
       <td align="center">
         <a href="https://github.com/philipgian">
           <img src="https://avatars.githubusercontent.com/u/6884633?v=3" width="100px;" alt="@philipgian" />
           <br />
           <sub>
             <b>Filippos Giannakos</b>
           </sub>
         </a>
         <br />
         <a href="https://github.com/search?q=repo%3Aakaihola%2Fdarkgraylib+repo%3Aakaihola%2Fdarker+author%3Aphilipgian&type=pullrequests" title="Code">💻</a>
       </td>
       <td align="center">
         <a href="https://github.com/foxwhite25">
           <img src="https://avatars.githubusercontent.com/u/39846845?v=3" width="100px;" alt="@foxwhite25" />
           <br />
           <sub>
             <b>Fox_white</b>
           </sub>
         </a>
         <br />
         <a href="https://github.com/search?q=repo%3Aakaihola%2Fdarkgraylib+repo%3Aakaihola%2Fdarker+foxwhite25" title="Bug reports">🐛</a>
       </td>
       <td align="center">
         <a href="https://github.com/gdiscry">
           <img src="https://avatars.githubusercontent.com/u/476823?v=3" width="100px;" alt="@gdiscry" />
           <br />
           <sub>
             <b>Georges Discry</b>
           </sub>
         </a>
         <br />
         <a href="https://github.com/search?q=repo%3Aakaihola%2Fdarkgraylib+repo%3Aakaihola%2Fdarker+author%3Agdiscry&type=pullrequests" title="Code">💻</a>
       </td>
       <td align="center">
         <a href="https://github.com/muggenhor">
           <img src="https://avatars.githubusercontent.com/u/484066?v=3" width="100px;" alt="@muggenhor" />
           <br />
           <sub>
             <b>Giel van Schijndel</b>
           </sub>
         </a>
         <br />
         <a href="https://github.com/search?q=repo%3Aakaihola%2Fdarkgraylib+repo%3Aakaihola%2Fdarker+author%3Amuggenhor&type=commits" title="Code">💻</a>
       </td>
       <td align="center">
         <a href="https://github.com/jabesq">
           <img src="https://avatars.githubusercontent.com/u/12049794?v=3" width="100px;" alt="@jabesq" />
           <br />
           <sub>
             <b>Hugo Dupras</b>
           </sub>
         </a>
         <br />
         <a href="https://github.com/search?q=repo%3Aakaihola%2Fdarkgraylib+repo%3Aakaihola%2Fdarker+author%3Ajabesq&type=pullrequests" title="Code">💻</a>
         <a href="https://github.com/search?q=repo%3Aakaihola%2Fdarkgraylib+repo%3Aakaihola%2Fdarker+author%3Ajabesq&type=issues" title="Bug reports">🐛</a>
       </td>
       <td align="center">
         <a href="https://github.com/hugovk">
           <img src="https://avatars.githubusercontent.com/u/1324225?v=3" width="100px;" alt="@hugovk" />
           <br />
           <sub>
             <b>Hugo van Kemenade</b>
           </sub>
         </a>
         <br />
         <a href="https://github.com/search?q=repo%3Aakaihola%2Fdarkgraylib+repo%3Aakaihola%2Fdarker+author%3Ahugovk&type=pullrequests" title="Code">💻</a>
       </td>
     </tr>
     <tr>
       <td align="center">
         <a href="https://github.com/irynahryshanovich">
           <img src="https://avatars.githubusercontent.com/u/62266480?v=3" width="100px;" alt="@irynahryshanovich" />
           <br />
           <sub>
             <b>Iryna</b>
           </sub>
         </a>
         <br />
         <a href="https://github.com/search?q=repo%3Aakaihola%2Fdarkgraylib+repo%3Aakaihola%2Fdarker+author%3Airynahryshanovich&type=issues" title="Bug reports">🐛</a>
       </td>
       <td align="center">
         <a href="https://github.com/yajo">
           <img src="https://avatars.githubusercontent.com/u/973709?v=3" width="100px;" alt="@yajo" />
           <br />
           <sub>
             <b>Jairo Llopis</b>
           </sub>
         </a>
         <br />
         <a href="https://github.com/search?q=repo%3Aakaihola%2Fdarkgraylib+repo%3Aakaihola%2Fdarker+commenter%3Ayajo&type=issues" title="Reviewed Pull Requests">👀</a>
       </td>
       <td align="center">
         <a href="https://github.com/jasleen19">
           <img src="https://avatars.githubusercontent.com/u/30443449?v=3" width="100px;" alt="@jasleen19" />
           <br />
           <sub>
             <b>Jasleen Kaur</b>
           </sub>
         </a>
         <br />
         <a href="https://github.com/search?q=repo%3Aakaihola%2Fdarkgraylib+repo%3Aakaihola%2Fdarker+author%3Ajasleen19&type=issues" title="Bug reports">🐛</a>
         <a href="https://github.com/search?q=repo%3Aakaihola%2Fdarkgraylib+repo%3Aakaihola%2Fdarker+reviewed-by%3Ajasleen19&type=pullrequests" title="Reviewed Pull Requests">👀</a>
       </td>
       <td align="center">
         <a href="https://github.com/jedie">
           <img src="https://avatars.githubusercontent.com/u/71315?v=3" width="100px;" alt="@jedie" />
           <br />
           <sub>
             <b>Jens Diemer</b>
           </sub>
         </a>
         <br />
         <a href="https://github.com/search?q=repo%3Aakaihola%2Fdarkgraylib+repo%3Aakaihola%2Fdarker+author%3Ajedie&type=issues" title="Bug reports">🐛</a>
       </td>
       <td align="center">
         <a href="https://github.com/jenshnielsen">
           <img src="https://avatars.githubusercontent.com/u/548266?v=3" width="100px;" alt="@jenshnielsen" />
           <br />
           <sub>
             <b>Jens Hedegaard Nielsen</b>
           </sub>
         </a>
         <br />
         <a href="https://github.com/search?q=repo%3Aakaihola%2Fdarkgraylib+repo%3Aakaihola%2Fdarker+jenshnielsen" title="Bug reports">🐛</a>
       </td>
       <td align="center">
         <a href="https://github.com/leej3">
           <img src="https://avatars.githubusercontent.com/u/5418152?v=3" width="100px;" alt="@leej3" />
           <br />
           <sub>
             <b>John lee</b>
           </sub>
         </a>
         <br />
         <a href="https://github.com/search?q=repo%3Aakaihola%2Fdarkgraylib+repo%3Aakaihola%2Fdarker+commenter%3Aleej3&type=issues" title="Bug reports">🐛</a>
       </td>
     </tr>
     <tr>
       <td align="center">
         <a href="https://github.com/wkentaro">
           <img src="https://avatars.githubusercontent.com/u/4310419?v=3" width="100px;" alt="@wkentaro" />
           <br />
           <sub>
             <b>Kentaro Wada</b>
           </sub>
         </a>
         <br />
         <a href="https://github.com/search?q=repo%3Aakaihola%2Fdarkgraylib+repo%3Aakaihola%2Fdarker+author%3Awkentaro&type=issues" title="Bug reports">🐛</a>
       </td>
       <td align="center">
         <a href="https://github.com/Asuskf">
           <img src="https://avatars.githubusercontent.com/u/36687747?v=3" width="100px;" alt="@Asuskf" />
           <br />
           <sub>
             <b>Kevin David</b>
           </sub>
         </a>
         <br />
         <a href="https://github.com/search?q=repo%3Aakaihola%2Fdarkgraylib+repo%3Aakaihola%2Fdarker+involves%3AAsuskf&type=discussions" title="Bug reports">🐛</a>
       </td>
       <td align="center">
         <a href="https://github.com/Krischtopp">
           <img src="https://avatars.githubusercontent.com/u/56152637?v=3" width="100px;" alt="@Krischtopp" />
           <br />
           <sub>
             <b>Krischtopp</b>
           </sub>
         </a>
         <br />
         <a href="https://github.com/search?q=repo%3Aakaihola%2Fdarkgraylib+repo%3Aakaihola%2Fdarker+author%3AKrischtopp&type=issues" title="Bug reports">🐛</a>
       </td>
       <td align="center">
         <a href="https://github.com/leotrs">
           <img src="https://avatars.githubusercontent.com/u/1096704?v=3" width="100px;" alt="@leotrs" />
           <br />
           <sub>
             <b>Leo Torres</b>
           </sub>
         </a>
         <br />
         <a href="https://github.com/search?q=repo%3Aakaihola%2Fdarkgraylib+repo%3Aakaihola%2Fdarker+author%3Aleotrs&type=issues" title="Bug reports">🐛</a>
       </td>
       <td align="center">
         <a href="https://github.com/Carreau">
           <img src="https://avatars.githubusercontent.com/u/335567?v=3" width="100px;" alt="@Carreau" />
           <br />
           <sub>
             <b>M Bussonnier</b>
           </sub>
         </a>
         <br />
         <a href="https://github.com/search?q=repo%3Aakaihola%2Fdarkgraylib+repo%3Aakaihola%2Fdarker+author%3ACarreau&type=commits" title="Code">💻</a>
         <a href="https://github.com/search?q=repo%3Aakaihola%2Fdarkgraylib+repo%3Aakaihola%2Fdarker+author%3ACarreau&type=commits" title="Documentation">📖</a>
         <a href="https://github.com/search?q=repo%3Aakaihola%2Fdarkgraylib+repo%3Aakaihola%2Fdarker+reviewed-by%3ACarreau&type=pullrequests" title="Reviewed Pull Requests">👀</a>
       </td>
       <td align="center">
         <a href="https://github.com/magnunm">
           <img src="https://avatars.githubusercontent.com/u/45951302?v=3" width="100px;" alt="@magnunm" />
           <br />
           <sub>
             <b>Magnus N. Malmquist</b>
           </sub>
         </a>
         <br />
         <a href="https://github.com/search?q=repo%3Aakaihola%2Fdarkgraylib+repo%3Aakaihola%2Fdarker+author%3Amagnunm&type=issues" title="Bug reports">🐛</a>
       </td>
     </tr>
     <tr>
       <td align="center">
         <a href="https://github.com/markddavidoff">
           <img src="https://avatars.githubusercontent.com/u/1360543?v=3" width="100px;" alt="@markddavidoff" />
           <br />
           <sub>
             <b>Mark Davidoff</b>
           </sub>
         </a>
         <br />
         <a href="https://github.com/search?q=repo%3Aakaihola%2Fdarkgraylib+repo%3Aakaihola%2Fdarker+author%3Amarkddavidoff&type=issues" title="Bug reports">🐛</a>
       </td>
       <td align="center">
         <a href="https://github.com/matclayton">
           <img src="https://avatars.githubusercontent.com/u/126218?v=3" width="100px;" alt="@matclayton" />
           <br />
           <sub>
             <b>Mat Clayton</b>
           </sub>
         </a>
         <br />
         <a href="https://github.com/search?q=repo%3Aakaihola%2Fdarkgraylib+repo%3Aakaihola%2Fdarker+author%3Amatclayton&type=issues" title="Bug reports">🐛</a>
       </td>
       <td align="center">
         <a href="https://github.com/MatthijsBurgh">
           <img src="https://avatars.githubusercontent.com/u/18014833?v=3" width="100px;" alt="@MatthijsBurgh" />
           <br />
           <sub>
             <b>Matthijs van der Burgh</b>
           </sub>
         </a>
         <br />
         <a href="https://github.com/search?q=repo%3Aakaihola%2Fdarkgraylib+repo%3Aakaihola%2Fdarker+author%3AMatthijsBurgh&type=issues" title="Bug reports">🐛</a>
       </td>
       <td align="center">
         <a href="https://github.com/minrk">
           <img src="https://avatars.githubusercontent.com/u/151929?v=3" width="100px;" alt="@minrk" />
           <br />
           <sub>
             <b>Min RK</b>
           </sub>
         </a>
         <br />
         <a href="https://github.com/search?q=repo%3Aconda-forge%2Fdarkgraylib-feedstock+OR+repo%3Aconda-forge%2Fdarker-feedstock+involves%3Aminrk&type=issues" title="Code">💻</a>
       </td>
       <td align="center">
         <a href="https://github.com/Mystic-Mirage">
           <img src="https://avatars.githubusercontent.com/u/1079805?v=3" width="100px;" alt="@Mystic-Mirage" />
           <br />
           <sub>
             <b>Mystic-Mirage</b>
           </sub>
         </a>
         <br />
         <a href="https://github.com/search?q=repo%3Aakaihola%2Fdarkgraylib+repo%3Aakaihola%2Fdarker+author%3AMystic-Mirage&type=commits" title="Code">💻</a>
         <a href="https://github.com/search?q=repo%3Aakaihola%2Fdarkgraylib+repo%3Aakaihola%2Fdarker+author%3AMystic-Mirage&type=commits" title="Documentation">📖</a>
         <a href="https://github.com/search?q=repo%3Aakaihola%2Fdarkgraylib+repo%3Aakaihola%2Fdarker+reviewed-by%3AMystic-Mirage&type=pullrequests" title="Reviewed Pull Requests">👀</a>
       </td>
       <td align="center">
         <a href="https://github.com/njhuffman">
           <img src="https://avatars.githubusercontent.com/u/66969728?v=3" width="100px;" alt="@njhuffman" />
           <br />
           <sub>
             <b>Nathan Huffman</b>
           </sub>
         </a>
         <br />
         <a href="https://github.com/search?q=repo%3Aakaihola%2Fdarkgraylib+repo%3Aakaihola%2Fdarker+author%3Anjhuffman&type=issues" title="Bug reports">🐛</a>
         <a href="https://github.com/search?q=repo%3Aakaihola%2Fdarkgraylib+repo%3Aakaihola%2Fdarker+author%3Anjhuffman&type=commits" title="Code">💻</a>
       </td>
     </tr>
     <tr>
       <td align="center">
         <a href="https://github.com/wasdee">
           <img src="https://avatars.githubusercontent.com/u/8089231?v=3" width="100px;" alt="@wasdee" />
           <br />
           <sub>
             <b>Nutchanon Ninyawee</b>
           </sub>
         </a>
         <br />
         <a href="https://github.com/search?q=repo%3Aakaihola%2Fdarkgraylib+repo%3Aakaihola%2Fdarker+author%3Awasdee&type=issues" title="Bug reports">🐛</a>
       </td>
       <td align="center">
         <a href="https://github.com/Pacu2">
           <img src="https://avatars.githubusercontent.com/u/21290461?v=3" width="100px;" alt="@Pacu2" />
           <br />
           <sub>
             <b>Pacu2</b>
           </sub>
         </a>
         <br />
         <a href="https://github.com/search?q=repo%3Aakaihola%2Fdarkgraylib+repo%3Aakaihola%2Fdarker+author%3APacu2&type=pullrequests" title="Code">💻</a>
         <a href="https://github.com/search?q=repo%3Aakaihola%2Fdarkgraylib+repo%3Aakaihola%2Fdarker+reviewed-by%3APacu2&type=pullrequests" title="Reviewed Pull Requests">👀</a>
       </td>
       <td align="center">
         <a href="https://github.com/PatrickJordanCongenica">
           <img src="https://avatars.githubusercontent.com/u/85236670?v=3" width="100px;" alt="@PatrickJordanCongenica" />
           <br />
           <sub>
             <b>Patrick Jordan</b>
           </sub>
         </a>
         <br />
         <a href="https://github.com/search?q=repo%3Aakaihola%2Fdarkgraylib+repo%3Aakaihola%2Fdarker+involves%3APatrickJordanCongenica&type=discussions" title="Bug reports">🐛</a>
       </td>
       <td align="center">
         <a href="https://github.com/ivanov">
           <img src="https://avatars.githubusercontent.com/u/118211?v=3" width="100px;" alt="@ivanov" />
           <br />
           <sub>
             <b>Paul Ivanov</b>
           </sub>
         </a>
         <br />
         <a href="https://github.com/search?q=repo%3Aakaihola%2Fdarkgraylib+repo%3Aakaihola%2Fdarker+author%3Aivanov&type=commits" title="Code">💻</a>
         <a href="https://github.com/search?q=repo%3Aakaihola%2Fdarkgraylib+repo%3Aakaihola%2Fdarker+author%3Aivanov&type=issues" title="Bug reports">🐛</a>
         <a href="https://github.com/search?q=repo%3Aakaihola%2Fdarkgraylib+repo%3Aakaihola%2Fdarker+reviewed-by%3Aivanov&type=pullrequests" title="Reviewed Pull Requests">👀</a>
       </td>
       <td align="center">
         <a href="https://github.com/flying-sheep">
           <img src="https://avatars.githubusercontent.com/u/291575?v=3" width="100px;" alt="@flying-sheep" />
           <br />
           <sub>
             <b>Philipp A.</b>
           </sub>
         </a>
         <br />
         <a href="https://github.com/search?q=repo%3Aakaihola%2Fdarkgraylib+repo%3Aakaihola%2Fdarker+author%3Aflying-sheep&type=issues" title="Bug reports">🐛</a>
       </td>
       <td align="center">
         <a href="https://github.com/RishiKumarRay">
           <img src="https://avatars.githubusercontent.com/u/87641376?v=3" width="100px;" alt="@RishiKumarRay" />
           <br />
           <sub>
             <b>Rishi Kumar Ray</b>
           </sub>
         </a>
         <br />
         <a href="https://github.com/search?q=repo%3Aakaihola%2Fdarkgraylib+repo%3Aakaihola%2Fdarker+RishiKumarRay" title="Bug reports">🐛</a>
       </td>
     </tr>
     <tr>
       <td align="center">
         <a href="https://github.com/ioggstream">
           <img src="https://avatars.githubusercontent.com/u/1140844?v=3" width="100px;" alt="@ioggstream" />
           <br />
           <sub>
             <b>Roberto Polli</b>
           </sub>
         </a>
         <br />
         <a href="https://github.com/search?q=repo%3Aakaihola%2Fdarkgraylib+repo%3Aakaihola%2Fdarker+commenter%3Aioggstream&type=issues" title="Bug reports">🐛</a>
       </td>
       <td align="center">
         <a href="https://github.com/roniemartinez">
           <img src="https://avatars.githubusercontent.com/u/2573537?v=3" width="100px;" alt="@roniemartinez" />
           <br />
           <sub>
             <b>Ronie Martinez</b>
           </sub>
         </a>
         <br />
         <a href="https://github.com/search?q=repo%3Aakaihola%2Fdarkgraylib+repo%3Aakaihola%2Fdarker+author%3Aroniemartinez&type=issues" title="Bug reports">🐛</a>
       </td>
       <td align="center">
         <a href="https://github.com/rossbar">
           <img src="https://avatars.githubusercontent.com/u/1268991?v=3" width="100px;" alt="@rossbar" />
           <br />
           <sub>
             <b>Ross Barnowski</b>
           </sub>
         </a>
         <br />
         <a href="https://github.com/search?q=repo%3Aakaihola%2Fdarkgraylib+repo%3Aakaihola%2Fdarker+author%3Arossbar&type=issues" title="Bug reports">🐛</a>
       </td>
       <td align="center">
         <a href="https://github.com/sherbie">
           <img src="https://avatars.githubusercontent.com/u/15087653?v=3" width="100px;" alt="@sherbie" />
           <br />
           <sub>
             <b>Sean Hammond</b>
           </sub>
         </a>
         <br />
         <a href="https://github.com/search?q=repo%3Aakaihola%2Fdarkgraylib+repo%3Aakaihola%2Fdarker+reviewed-by%3Asherbie&type=pullrequests" title="Reviewed Pull Requests">👀</a>
       </td>
       <td align="center">
         <a href="https://github.com/hauntsaninja">
           <img src="https://avatars.githubusercontent.com/u/12621235?v=3" width="100px;" alt="@hauntsaninja" />
           <br />
           <sub>
             <b>Shantanu</b>
           </sub>
         </a>
         <br />
         <a href="https://github.com/search?q=repo%3Aakaihola%2Fdarkgraylib+repo%3Aakaihola%2Fdarker+author%3Ahauntsaninja&type=issues" title="Bug reports">🐛</a>
       </td>
       <td align="center">
         <a href="https://github.com/simgunz">
           <img src="https://avatars.githubusercontent.com/u/466270?v=3" width="100px;" alt="@simgunz" />
           <br />
           <sub>
             <b>Simone Gaiarin</b>
           </sub>
         </a>
         <br />
         <a href="https://github.com/search?q=repo%3Aakaihola%2Fdarkgraylib+repo%3Aakaihola%2Fdarker+commenter%3Asimgunz&type=issues" title="Reviewed Pull Requests">👀</a>
       </td>
     </tr>
     <tr>
       <td align="center">
         <a href="https://github.com/soxofaan">
           <img src="https://avatars.githubusercontent.com/u/44946?v=3" width="100px;" alt="@soxofaan" />
           <br />
           <sub>
             <b>Stefaan Lippens</b>
           </sub>
         </a>
         <br />
         <a href="https://github.com/search?q=repo%3Aakaihola%2Fdarkgraylib+repo%3Aakaihola%2Fdarker+author%3Asoxofaan&type=pullrequests" title="Documentation">📖</a>
       </td>
       <td align="center">
         <a href="https://github.com/Svenito">
           <img src="https://avatars.githubusercontent.com/u/31278?v=3" width="100px;" alt="@Svenito" />
           <br />
           <sub>
             <b>Sven Steinbauer</b>
           </sub>
         </a>
         <br />
         <a href="https://github.com/search?q=repo%3Aakaihola%2Fdarkgraylib+repo%3Aakaihola%2Fdarker+author%3ASvenito&type=pullrequests" title="Code">💻</a>
       </td>
       <td align="center">
         <a href="https://github.com/tkolleh">
           <img src="https://avatars.githubusercontent.com/u/3095197?v=3" width="100px;" alt="@tkolleh" />
           <br />
           <sub>
             <b>TJ Kolleh</b>
           </sub>
         </a>
         <br />
         <a href="https://github.com/search?q=repo%3Aakaihola%2Fdarkgraylib+repo%3Aakaihola%2Fdarker+author%3Atkolleh&type=issues" title="Bug reports">🐛</a>
       </td>
       <td align="center">
         <a href="https://github.com/talhajunaidd">
           <img src="https://avatars.githubusercontent.com/u/6547611?v=3" width="100px;" alt="@talhajunaidd" />
           <br />
           <sub>
             <b>Talha Juanid</b>
           </sub>
         </a>
         <br />
         <a href="https://github.com/search?q=repo%3Aakaihola%2Fdarkgraylib+repo%3Aakaihola%2Fdarker+author%3Atalhajunaidd&type=commits" title="Code">💻</a>
       </td>
       <td align="center">
         <a href="https://github.com/guettli">
           <img src="https://avatars.githubusercontent.com/u/414336?v=3" width="100px;" alt="@guettli" />
           <br />
           <sub>
             <b>Thomas Güttler</b>
           </sub>
         </a>
         <br />
         <a href="https://github.com/search?q=repo%3Aakaihola%2Fdarkgraylib+repo%3Aakaihola%2Fdarker+author%3Aguettli&type=issues" title="Bug reports">🐛</a>
       </td>
       <td align="center">
         <a href="https://github.com/tobiasdiez">
           <img src="https://avatars.githubusercontent.com/u/5037600?v=3" width="100px;" alt="@tobiasdiez" />
           <br />
           <sub>
             <b>Tobias Diez</b>
           </sub>
         </a>
         <br />
       </td>
     </tr>
     <tr>
       <td align="center">
         <a href="https://github.com/tgross35">
           <img src="https://avatars.githubusercontent.com/u/13724985?v=3" width="100px;" alt="@tgross35" />
           <br />
           <sub>
             <b>Trevor Gross</b>
           </sub>
         </a>
         <br />
         <a href="https://github.com/search?q=repo%3Aakaihola%2Fdarkgraylib+repo%3Aakaihola%2Fdarker+author%3Atgross35&type=issues" title="Bug reports">🐛</a>
       </td>
       <td align="center">
         <a href="https://github.com/victorcui96">
           <img src="https://avatars.githubusercontent.com/u/14048976?v=3" width="100px;" alt="@victorcui96" />
           <br />
           <sub>
             <b>Victor Cui</b>
           </sub>
         </a>
         <br />
         <a href="https://github.com/search?q=repo%3Aakaihola%2Fdarkgraylib+repo%3Aakaihola%2Fdarker+commenter%3Avictorcui96&type=issues" title="Bug reports">🐛</a>
       </td>
       <td align="center">
         <a href="https://github.com/yoursvivek">
           <img src="https://avatars.githubusercontent.com/u/163296?v=3" width="100px;" alt="@yoursvivek" />
           <br />
           <sub>
             <b>Vivek Kushwaha</b>
           </sub>
         </a>
         <br />
         <a href="https://github.com/search?q=repo%3Aakaihola%2Fdarkgraylib+repo%3Aakaihola%2Fdarker+author%3Ayoursvivek&type=issues" title="Bug reports">🐛</a>
         <a href="https://github.com/search?q=repo%3Aakaihola%2Fdarkgraylib+repo%3Aakaihola%2Fdarker+author%3Ayoursvivek&type=commits" title="Documentation">📖</a>
       </td>
       <td align="center">
         <a href="https://github.com/Hainguyen1210">
           <img src="https://avatars.githubusercontent.com/u/15359217?v=3" width="100px;" alt="@Hainguyen1210" />
           <br />
           <sub>
             <b>Will</b>
           </sub>
         </a>
         <br />
         <a href="https://github.com/search?q=repo%3Aakaihola%2Fdarkgraylib+repo%3Aakaihola%2Fdarker+author%3AHainguyen1210&type=issues" title="Bug reports">🐛</a>
       </td>
       <td align="center">
         <a href="https://github.com/wjdp">
           <img src="https://avatars.githubusercontent.com/u/1690934?v=3" width="100px;" alt="@wjdp" />
           <br />
           <sub>
             <b>Will Pimblett</b>
           </sub>
         </a>
         <br />
         <a href="https://github.com/search?q=repo%3Aakaihola%2Fdarkgraylib+repo%3Aakaihola%2Fdarker+author%3Awjdp&type=issues" title="Bug reports">🐛</a>
         <a href="https://github.com/search?q=repo%3Aakaihola%2Fdarkgraylib+repo%3Aakaihola%2Fdarker+author%3Awjdp&type=pullrequests" title="Documentation">📖</a>
       </td>
       <td align="center">
         <a href="https://github.com/wpnbos">
           <img src="https://avatars.githubusercontent.com/u/33165624?v=3" width="100px;" alt="@wpnbos" />
           <br />
           <sub>
             <b>William Bos</b>
           </sub>
         </a>
         <br />
         <a href="https://github.com/search?q=repo%3Aakaihola%2Fdarkgraylib+repo%3Aakaihola%2Fdarker+author%3Awpnbos&type=issues" title="Bug reports">🐛</a>
       </td>
     </tr>
     <tr>
       <td align="center">
         <a href="https://github.com/zachnorton4C">
           <img src="https://avatars.githubusercontent.com/u/49661202?v=3" width="100px;" alt="@zachnorton4C" />
           <br />
           <sub>
             <b>Zach Norton</b>
           </sub>
         </a>
         <br />
         <a href="https://github.com/search?q=repo%3Aakaihola%2Fdarkgraylib+repo%3Aakaihola%2Fdarker+author%3Azachnorton4C&type=issues" title="Bug reports">🐛</a>
       </td>
       <td align="center">
         <a href="https://github.com/deadkex">
           <img src="https://avatars.githubusercontent.com/u/59506422?v=3" width="100px;" alt="@deadkex" />
           <br />
           <sub>
             <b>deadkex</b>
           </sub>
         </a>
         <br />
         <a href="https://github.com/search?q=repo%3Aakaihola%2Fdarkgraylib+repo%3Aakaihola%2Fdarker+involves%3Adeadkex&type=discussions" title="Bug reports">🐛</a>
       </td>
       <td align="center">
         <a href="https://github.com/dsmanl">
           <img src="https://avatars.githubusercontent.com/u/67360039?v=3" width="100px;" alt="@dsmanl" />
           <br />
           <sub>
             <b>dsmanl</b>
           </sub>
         </a>
         <br />
         <a href="https://github.com/search?q=repo%3Aakaihola%2Fdarkgraylib+repo%3Aakaihola%2Fdarker+author%3Adsmanl&type=issues" title="Bug reports">🐛</a>
       </td>
       <td align="center">
         <a href="https://github.com/jsuit">
           <img src="https://avatars.githubusercontent.com/u/1467906?v=3" width="100px;" alt="@jsuit" />
           <br />
           <sub>
             <b>jsuit</b>
           </sub>
         </a>
         <br />
         <a href="https://github.com/search?q=repo%3Aakaihola%2Fdarkgraylib+repo%3Aakaihola%2Fdarker+involves%3Ajsuit&type=discussions" title="Bug reports">🐛</a>
       </td>
       <td align="center">
         <a href="https://github.com/martinRenou">
           <img src="https://avatars.githubusercontent.com/u/21197331?v=3" width="100px;" alt="@martinRenou" />
           <br />
           <sub>
             <b>martinRenou</b>
           </sub>
         </a>
         <br />
         <a href="https://github.com/search?q=repo%3Aconda-forge%2Fstaged-recipes+akaihola%2Fdarkgraylib+OR+akaihola%2Fdarker+involves%3AmartinRenou&type=pullrequests" title="Code">💻</a>
         <a href="https://github.com/search?q=repo%3Aakaihola%2Fdarkgraylib+repo%3Aakaihola%2Fdarker+reviewed-by%3AmartinRenou&type=pullrequests" title="Reviewed Pull Requests">👀</a>
       </td>
       <td align="center">
         <a href="https://github.com/mayk0gan">
           <img src="https://avatars.githubusercontent.com/u/96263702?v=3" width="100px;" alt="@mayk0gan" />
           <br />
           <sub>
             <b>mayk0gan</b>
           </sub>
         </a>
         <br />
         <a href="https://github.com/search?q=repo%3Aakaihola%2Fdarkgraylib+repo%3Aakaihola%2Fdarker+author%3Amayk0gan&type=issues" title="Bug reports">🐛</a>
       </td>
     </tr>
     <tr>
       <td align="center">
         <a href="https://github.com/okuuva">
           <img src="https://avatars.githubusercontent.com/u/2804020?v=3" width="100px;" alt="@okuuva" />
           <br />
           <sub>
             <b>okuuva</b>
           </sub>
         </a>
         <br />
         <a href="https://github.com/search?q=repo%3Aakaihola%2Fdarkgraylib+repo%3Aakaihola%2Fdarker+commenter%3Aokuuva&type=issues" title="Bug reports">🐛</a>
       </td>
       <td align="center">
         <a href="https://github.com/overratedpro">
           <img src="https://avatars.githubusercontent.com/u/1379994?v=3" width="100px;" alt="@overratedpro" />
           <br />
           <sub>
             <b>overratedpro</b>
           </sub>
         </a>
         <br />
         <a href="https://github.com/search?q=repo%3Aakaihola%2Fdarkgraylib+repo%3Aakaihola%2Fdarker+author%3Aoverratedpro&type=issues" title="Bug reports">🐛</a>
       </td>
       <td align="center">
         <a href="https://github.com/simonf-dev">
           <img src="https://avatars.githubusercontent.com/u/52134089?v=3" width="100px;" alt="@simonf-dev" />
           <br />
           <sub>
             <b>sfoucek</b>
           </sub>
         </a>
         <br />
         <a href="https://github.com/search?q=repo%3Aakaihola%2Fdarkgraylib+repo%3Aakaihola%2Fdarker+commenter%3Asimonf-dev&type=issues" title="Bug reports">🐛</a>
       </td>
       <td align="center">
         <a href="https://github.com/rogalski">
           <img src="https://avatars.githubusercontent.com/u/9485217?v=3" width="100px;" alt="@rogalski" />
           <br />
           <sub>
             <b>Łukasz Rogalski</b>
           </sub>
         </a>
         <br />
         <a href="https://github.com/search?q=repo%3Aakaihola%2Fdarkgraylib+repo%3Aakaihola%2Fdarker+author%3Arogalski&type=pullrequests" title="Code">💻</a>
         <a href="https://github.com/search?q=repo%3Aakaihola%2Fdarkgraylib+repo%3Aakaihola%2Fdarker+author%3Arogalski&type=issues" title="Bug reports">🐛</a>
       </td>
     </tr>
   </table>   <!-- ALL-CONTRIBUTORS-LIST:END -->

This project follows the all-contributors_ specification.
Contributions of any kind are welcome!

.. _README.rst: https://github.com/akaihola/darkgraylib/blob/main/README.rst
.. _emoji key: https://allcontributors.org/docs/en/emoji-key
.. _all-contributors: https://allcontributors.org


GitHub stars trend
==================

|stargazers|_

.. |stargazers| image:: https://starchart.cc/akaihola/darkgraylib.svg
.. _stargazers: https://starchart.cc/akaihola/darkgraylib
