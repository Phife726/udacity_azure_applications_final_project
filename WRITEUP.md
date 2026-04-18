## CMS Deployment Strategy

To deploy the app, we compared two main options: a Virtual Machine (VM) and Azure App Service. Here’s how they stack up.

### 1. Cost

A VM has a predictable monthly cost based on the size you choose, but you end up paying for resources even when you’re not using them. On top of that, things like storage, IP addresses, and the time spent maintaining the server add to the real cost.

App Service uses a tiered pricing model, and for this project, the lower tiers (like Free or Basic) are enough to get started. While it can look slightly more expensive at first glance, it includes a lot out of the box like the operating system, runtime, and security updates. That means less time spent on maintenance and a lower overall cost in practice.

### 2. Scalability

Scaling a VM takes effort. If you want more power, you often need to resize it, which can cause downtime. If you want multiple instances, you have to set up load balancing and other infrastructure yourself.

App Service makes scaling much easier. You can increase resources or add more instances with just a few clicks, or even automate it based on usage.

### 3. Availability

With a VM, high availability is something you have to design and manage yourself. That usually means running multiple instances and configuring them properly.

App Service handles this for you. It’s built to keep your app running without requiring extra setup, so you get better reliability with less work.

### 4. Workflow (Ease of Use)

Using a VM is more hands-on. You need to connect to the server, install and configure everything, and manage updates yourself.

App Service is much simpler. It integrates directly with GitHub, so every time you push code, it can automatically build and deploy your app. This makes development faster and more consistent.

### Final Choice: Azure App Service

Azure App Service is the better option for this project. It removes the need to manage servers, simplifies deployment, and makes scaling and maintenance much easier. That lets you spend more time building the application and less time dealing with infrastructure.

### Assess app changes that would change your decision.

The decision would shift away from Azure App Service if the application required greater control over the operating system, more complex or legacy architecture, or advanced networking and security configurations. It would also change if the workload became consistently high enough to favor a VM from a cost perspective, or if deployments required highly customized workflows.

Summary: App Service is ideal for standard, scalable web apps, but a VM becomes the better choice when control, complexity, or customization significantly increase.